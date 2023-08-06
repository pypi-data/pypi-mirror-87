"""
This module implements a class to make queries to AWS Redshift database.
It supports an API to download commerce and transactional data.
"""
from datetime import date
import re
import ast
import pandas as pd
from sqlalchemy import create_engine

class Redshift:
    """
    The Redshift class purpose is to provide a standard API to query AWS Redshift
    database to gather data and create suggestions.

    All queries uses the atribute `customer_id` to filter customer's data.

    Args:
        customer_id (str): YOM's unique identifier for each customer.
        query_filter (str): Parsed dict with filter query.
        job_id (str): Strategy id used to download objects from s3

    Attributes:
        customer_id (str): YOM's unique identifier for each customer.
        query_filter (str): Parsed dict with filter query.
        conn_str (str): Redhisft connection string
        job_id (str): Strategy id used to download objects from s3
    """

    def __init__(self, customer_id, query_filter, connection_str, job_id=None):
        self.customer_id = customer_id
        self.conn_str = connection_str
        self.job_id = job_id
        self.query_filter = query_filter
        self.__process_query_filter()

    def __process_query_filter(self) -> None:
        """
        Set the query filter to a functional dictionary.
        Attributes:
            query_filter: query filter.
        """
        self.query_filter = self.query_filter.replace('products_segments', 'data_science.products_segments')
        self.query_filter = ast.literal_eval(self.query_filter) if bool(self.query_filter) else {}
        # Delete empty filters
        for key in list(self.query_filter):
            if not self.query_filter[key]:
                self.query_filter.pop(key)

    def __escape_characters(self, operation):
        """
        Escape a single quoation mark, adding another single and
        replacing double quoations marks by single.

        Args:
            operation (list): Represent the items inside  redshidt key to filter.
        return:
            parsed_operation (str): String with escaped characters.

        """
        # Identify string closed with double quoation marks
        matches = re.findall(r'\"(.+?)\"', str(operation))

        # Replace by valid quoation marks
        operation = [i for i in operation if i not in matches]
        matches = [i.replace("'", "''") for i in matches]

        return f"""  ('{"','".join(matches + operation)}') """

    def __set_unions_on_queries(self, entity: str, origin_table: str) -> str:
        """
        Create the query structure dedicated to unions.

        Args:
            entity (str): Redshift entity used to filter.
        Return:
            join (str): Structure of join in query.
        """
        # Entity : ('Attribute to merge', 'Join method')
        relation_entity_filter = {
            'commerces' : ('userid', 'JOIN'),
            'products': ('productid', 'JOIN'),
            'data_science.products_segments': ('productid', 'LEFT JOIN'),
            'orders' : ('userid', 'INNER JOIN'),
            'sellers': ('userid', 'INNER JOIN')
        }
        join_method = relation_entity_filter[f'{entity}'][1]
        attribute = relation_entity_filter[f'{entity}'][0]
        join = f""" {join_method}(
            select *
            from {entity}
            where customerid = '{self.customer_id}'
            ) {entity.split('.')[-1]}
            ON {origin_table}.{attribute} = {entity}.{attribute} """

        return join

    def __parse_joins(self, query: str) -> tuple:
        """
        It Sets the "joins" that will use the query.
        Args:
            query (str): Raw query.
        Return:
            query (str): Query with a join structure.
            keys_filter (list): Entities used in constraints.
        """
        # Identify origin table
        idx_from_table = query.upper().split(' ').index('FROM') + 1
        origin_table = query.split(' ')[idx_from_table]

        # Interactions between origin tables and their joins. from_table: [join_tables]
        join_interactions = {
            'orders': ['commerces', 'products', 'data_science.products_segments'],
            'products': ['data_science.products_segments'],
            'commerces': ['data_science.commerces_clusters'],
            'suggestions': ['commerces', 'products', 'orders'],
            'sellers': ['commerces']}

        # Keys wich the query will interact
        joins = ' '
        # Intersection between possible interactions and keys in query filter
        keys_filter = [i for i in self.query_filter.keys() if (i != origin_table) and (i in join_interactions[origin_table])]
        for entity in keys_filter:
            joins = joins + self.__set_unions_on_queries(entity, origin_table)

        # TODO: Change method to replace.
        # Index after 'from origin_table'
        index = query.upper().find('FROM') + len(origin_table) + 5
        query = query[:index] + joins + query[index:]
        keys_filter.append(origin_table)

        return query, keys_filter

    def __parse_query(self, base_query, entities=None):
        """
        Parse the query based on the attribute "query_filter".

        Args:
            base_query (str): base query to parse
            entities ([srt]) [Optional]: array to filter valid entities.

        Returns:
            query (str): parsed query.
        """
        if not bool(self.query_filter):
            return base_query

        # Apply filters
        for entity in self.query_filter.keys():
            # Skip loop if entity not in entities array
            if entities and entity not in entities:
                continue
            for key in self.query_filter[entity].keys():
                for operation in self.query_filter[entity][key].keys():
                    if not self.query_filter[entity][key][operation]:
                        continue
                    if operation == 'in':
                        operation_filter = self.__escape_characters(self.query_filter[entity][key][operation])
                        base_query = base_query + f"""AND {entity}.{key} in {operation_filter} \n"""
                    elif operation == 'not_in':
                        operation_filter = self.__escape_characters(self.query_filter[entity][key][operation])
                        # Fix to deal with null values in left joins.
                        if entity in ['data_science.products_segments']:
                            base_query = base_query + f"""and {entity.split('.')[-1]}.{key} is null or not null """
                        base_query = base_query + f"""AND {entity.split('.')[-1]}.{key}  not in {operation_filter} \n"""
                    else:
                        # TODO: Log exception as error
                        raise Exception(f'Invalid operation "{operation}"')

        # Fix 1 value arrays
        base_query = base_query.replace(',)', ')')

        return base_query


    def query_orders(self, from_date, to_date):
        """
        Download orders from AWS Redshift using a range of dates and the class
        customer_id parameter.

        :param from_date: Beginning date to filter data. Uses %Y-%m-%d format (ex: '2018-01-25').
        :param to_date: End date to filter data. Uses %Y-%m-%d format (ex: '2018-01-25').
        :return: Dataframe with transactional data.
        :rtype: Pandas Dataframe object.
        """
        query = f"""
                SELECT
                    orders.userid as user_id,
                    orders.productid as product_id,
                    orders.quantity as quantity,
                    orders.orderdt as date,
                    orders.priceperunit as price_per_unit,
                    commerces.supervisorid as supervisor_id
                FROM orders 
                WHERE orders.customerid = '{self.customer_id}'
                    AND (orders.orderdt between '{from_date}' and dateadd(day, -1, '{to_date}'))
            """
        query, entities = self.__parse_joins(query)
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            # Query orders
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        # Check if there is any map_file
        df = self.check_map_file(df, to_date)
        return df

    def query_commerces(self):
        """
        Download commerces from AWS Redshift using the class customer_id parameter.

        :return: Dataframe with commerce data.
        :rtype: Pandas Dataframe object.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT
                    userid as user_id,
                    sellerid as seller_id,
                    supervisorid as supervisor_id
                FROM commerces 
                WHERE commerces.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        return df

    def query_custom_commerces(self, str_filter):
        """
        Download custom query commerces from AWS Redshift using the class customer_id parameter.

        Args:
            field_sql_filter (list): Fields to SELECT in sql query.
        Returns:
            df (pd.DF): DataFrame with filtered commerces.
        """
        str_filter = ",".join(str_filter)
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT {str_filter}, userid as user_id
                FROM commerces 
                WHERE commerces.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        return df

    def query_products(self, to_date=None) -> pd.DataFrame:
        """
        Download products from AWS Redshift using the class customer_id parameter.

        :return: Dataframe with commerce data.
        :rtype: Pandas Dataframe object.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT
                    products.productid as product_id,
                    boxunit,
                    subcategory,
                    brand,
                    category,
                    name,
                    sku,
                    packageunit,
                    amountperpackage,
                    amountperbox,
                    blocked,
                    categoricallevel1,
                    categoricallevel3
                FROM products 
                WHERE products.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)
            df = self.check_map_file(df, to_date)
        return df

    def n_buy(self, from_date, to_date):
        """
        Get the times that a SKU has been buyed by a user in
        a selected period.

        Return
            df (pd.DF): DataFrame with user-sku-times buyed
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT orders.userid as user_id, orders.productid as product_id, count(orderdt) as buyed, sum(orders.quantity) as acc_quantity
                FROM orders 
                WHERE orders.customerid='{self.customer_id}'
                AND orderdt BETWEEN '{from_date}' and dateadd(day, -1, '{to_date}')
                """
            query, _ = self.__parse_joins(query)
            query = self.__parse_query(query, entities=['orders', 'commerces', 'products'])
            query = query + ' GROUP by orders.userid, orders.productid '
            df = pd.read_sql(query, conn)
        return df

    def n_suggestions(self, from_date, to_date):
        """
        Get the times that a SKU has been suggested by a user in
        a selected period.

        Return
            df (pd.DF): DataFrame with user-sku-times suggested
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT suggestions.userid as user_id, suggestions.productid as product_id, count(distinct suggestiondt) as suggested
                FROM suggestions
                INNER JOIN (
                    select *
                    from orders
                    where customerid = '{self.customer_id}'
                ) orders
                on orders.userid= suggestions.userid
                and suggestions.suggestiondt = orders.orderdt
                INNER JOIN (
                    select *
                    from commerces
                    where customerid = '{self.customer_id}'
                ) commerces
                on commerces.userid = suggestions.userid
                INNER JOIN (
                    select *
                    from products
                    where customerid = '{self.customer_id}'
                ) products
                ON products.productid = suggestions.productid
                WHERE orders.customerid='{self.customer_id}'
                AND suggestiondt BETWEEN '{from_date}' and dateadd(day, -1, '{to_date}')
                """
            query = self.__parse_query(query, entities=['orders', 'commerces', 'products'])
            query = query + ' GROUP by suggestions.userid, suggestions.productid '
            df = pd.read_sql(query, conn)

        return df

    def query_user_popular(self, from_date, to_date):
        """
        Makes a query and retrieve the user/product popularity.
        The popularity is how many times the user has bought the
        product within the input dates.

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results. The columns
            of the dataframe are user_id, product_id and popularity
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                select distinct orders.userid as user_id,
                    orders.productid as product_id,
                    count(*) as popularity
                from orders 
                where orders.customerid = '{self.customer_id}'
                    and orderdt between '{from_date}' and dateadd(day, -1, '{to_date}')
                    and quantity > 0
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            query += 'group by orders.userid, orders.productid'
            df = pd.read_sql(query, conn)

        return df

    def query_buy_dates(self, from_date, to_date):
        """
        Makes a query to retrieve concretion dates

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results. The columns
            of the dataframe are user_id and orderdt
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                select distinct orders.userid as user_id, orderdt
                from orders 
                where orders.customerid = '{self.customer_id}'
                    and orderdt between '{from_date}' and dateadd(day, -1, '{to_date}')
                    and quantity > 0
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            query += 'order by orders.userid, orderdt asc'
            df = pd.read_sql(query, conn)

        return df

    def query_commerces_feaures(self, from_date, to_date, disaggregated=False):
        """
        Makes a query to compute mean order features.

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            sub_query = f"""
                select orders.userid, orders.orderdt,
                    sum(quantity * priceperunit) as order_value,
                    count(distinct orders.productid) as order_amplitud,
                    sum(quantity) as order_depth
                from orders 
                where orders.customerid = '{self.customer_id}'
                    and orderdt between '{from_date}' and dateadd(day, -1, '{to_date}')
                    and quantity > 0
            """
            sub_query, entities = self.__parse_joins(sub_query)
            sub_query = self.__parse_query(sub_query, entities=entities)
            sub_query += 'group by orders.userid, orders.orderdt'

            query = f"""
                select orders.userid as user_id,
                    avg(order_value) as mean_order_value,
                    avg(order_amplitud) as mean_order_amplitud,
                    avg(order_depth) as mean_order_depth,
                    stddev(order_value) as std_order_value,
                    stddev(order_amplitud) as std_order_amplitud,
                    stddev(order_depth) as std_order_depth
                from (
                    {sub_query}
                ) orders
                group by orders.userid
            """

            if disaggregated:
                df = pd.read_sql(sub_query, conn).rename(columns={'userid':'user_id'})
            else:
                df = pd.read_sql(query, conn)

        return df

    def query_commerce_categories(self):
        """
        Makes a query to retrieve commerce categorical data.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                select userid as user_id,
                    sellerid as seller_id,
                    supervisorid as supervisor_id,
                    commune,
                    channel,
                    subchannel,
                    administrativelevel1,
                    administrativelevel2,
                    administrativelevel3,
                    class
                from commerces 
                where commerces.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        return df

    def query_product_categories(self):
        """
        Makes a query to retrieve products categorical data.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                select products.productid as product_id,
                    category,
                    subcategory,
                    brand
                from products 
                where products.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        return df

    def query_last_order_metadata(self, from_date, to_date):
        """
        Makes a query to retrieve last order metadata such as
        last quantity and last time the user bought the product.

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            # Generate a Common Table Expressions to query the last date
            # a user bought a product
            sub_query = f"""
                select orders.userid, orders.productid, max(orders.orderdt) as last_date
                from orders 
                where orders.customerid = '{self.customer_id}'
                    and orders.orderdt between '{from_date}' and dateadd(day, -1, '{to_date}')
            """
            sub_query, entities = self.__parse_joins(sub_query)
            sub_query = self.__parse_query(sub_query, entities=entities)
            sub_query += 'group by orders.userid, orders.productid'

            # Join the Common Table Expressions with orders
            query = f"""
                with last_buy as (sub_query)
                select distinct orders.userid as user_id,
                    orders.productid as product_id,
                    orders.orderdt as last_date,
                    orders.quantity as last_quantity,
                    orders.discountperunit 
                from orders 
                join last_buy
                    on last_buy.userid = orders.userid
                    and last_buy.productid = orders.productid
                    and last_buy.last_date = orders.orderdt
                where orders.customerid = '{self.customer_id}'
                    and orderdt between '{from_date}' and dateadd(day, -1, '{to_date}')
                """
            query, entities = self.__parse_joins(query)
            # Deal with partial formatting strings.
            query = query.replace('sub_query', sub_query)
            query = self.__parse_query(query, entities=entities)
            df = pd.read_sql(query, conn)

        return df

    def query_sellers(self):
        """
        Download sellers from AWS Redshift using the class customer_id parameter.

        Return:
            df(pd.DataFrame): Dataframe with seller data.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            query = f"""
                SELECT
                    sellers.userid as user_id,
                    sellers.sellerid as seller_id,
                    sellers.supervisorid as supervisor_id
                FROM sellers 
                WHERE sellers.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities)
            df = pd.read_sql(query, conn)
        return df

    def query_recurrent_cluster(self):
        """
        Makes a query to retrieve the clusterid of each user and
        their keys values.

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            # Query orders
            query = f"""
                SELECT 
                    table.userid as user_id,
                    table.clusterid as cluster_id,
                    table.productid as product_id,
                    table.T as period,
                    table.value as value
                FROM table
                INNER JOIN (
                    select *
                    from commerces
                    where commerces.customerid = '{self.customer_id}'
                ) commerces
                ON commerces.userid = orders.userid
                WHERE table.customerid = '{self.customer_id}'
                AND table.active = 1
                """
            query = self.__parse_query(query, entities=['table', 'commerces'])
            df = pd.read_sql(query, conn)

        return df

    def query_last_visit(self):
        """
        Makes a query to retrieve last order date.

        Args:
            from_date (str): From date to query. Format: %Y-%m-%d.
            to_date (str): To date to query. Format: %Y-%m-%d.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            # Generate a Common Table Expressions to query the last date
            # a user bought a product
            query = f"""
                select orders.userid, max(orders.orderdt) as last_date
                from orders 
                where orders.customerid = '{self.customer_id}'
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            query += 'group by orders.userid'

            df = pd.read_sql(query, conn)

        return df

    def query_prices(self, from_date=None, to_date=None):
        """
        Download orders from AWS Redshift using a range of dates and the class
        customer_id parameter.

        :param from_date: Beginning date to filter data. Uses %Y-%m-%d format (ex: '2018-01-25').
        :param to_date: End date to filter data. Uses %Y-%m-%d format (ex: '2018-01-25').
        :return: Dataframe with transactional data.
        :rtype: Pandas Dataframe object.
        """

        if to_date is None:
            to_date = str(pd.to_datetime('today') + pd.DateOffset(months=3))[:10]

        if from_date is None:
            from_date = str(pd.to_datetime(to_date) + pd.DateOffset(months=3))[:10]

        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            # Query orders
            query = f"""
                SELECT
                    orders.userid as user_id,
                    orders.productid as product_id,
                    avg(orders.priceperunit) as price_per_unit
                FROM orders 
                WHERE orders.customerid = '{self.customer_id}'
                    AND (orders.orderdt between '{from_date}' and dateadd(day, -1, '{to_date}'))
            """
            query, entities = self.__parse_joins(query)
            query = self.__parse_query(query, entities=entities)
            query += """group by orders.userid, orders.productid"""
            df = pd.read_sql(query, conn)

        return df

    def saf_filter(self, saf):
        """
        Get all posible combinations of users and products
        given by a Strategic Assignation File (saf).

        Parameter:
            saf (DataFrame): DataFrame with filter associated to commerces and products properties (redshift's columns).

        Return
            df (DataFrame): DataFrame with the cross join posible combinations.
        """
        saf_columns = saf.columns.tolist()
        target_col = saf_columns[-1]

        # Add userid and productid if not in assignation file, to use in the selection
        if 'commerces.userid' not in saf_columns and 'public.commerces.userid' not in saf_columns:
            saf_columns.append('commerces.userid')
        if 'products.productid' not in saf_columns and 'public.products.productid' not in saf_columns:
            saf_columns.append('products.productid')

        c_columns = [s for s in saf_columns if 'data_science.commerces_clusters' in s]

        p_columns = [s for s in saf_columns if 'data_science.products_segments' in s]

        query_select = f"""select distinct public.commerces.userid as userid, public.products.productid as productid """
        if target_col != 'public.products.productid':
            query_select = query_select + f""", {target_col}"""

        if len(c_columns) > 0:
            tmp_cols = [s for s in c_columns if s != target_col]
            if len(tmp_cols) != 0:
                query_select = query_select + ', ' + ','.join(tmp_cols)

        if len(p_columns) > 0:
            tmp_cols = [s for s in p_columns if s != target_col]
            if len(tmp_cols) != 0:
                query_select = query_select + ', ' + ','.join(tmp_cols)

        query = f"""
            {query_select}
            from public.products
            cross join public.commerces"""

        if len(c_columns) > 0:
            query = query + """ join data_science.commerces_clusters
            on data_science.commerces_clusters.userid = public.commerces.userid
            and data_science.commerces_clusters.customerid = public.commerces.customerid
            """

        if len(p_columns) > 0:
            query = query + """ join data_science.products_segments
            on data_science.products_segments.productid = public.products.productid
            and data_science.products_segments.customerid = public.products.customerid
            """

        query = query + f"""
            where public.products.customerid = '{self.customer_id}'
        """

        # Add restrictions inherent to SAF file
        for col in saf.columns:
            query = query + (f""" and {col} in {tuple(saf[col].unique())} \n""")
        query = self.__parse_query(query, entities=['commerces', 'products', 'products_segments', 'commerces_clusters'])

        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            conn.close()

        # TODO: Change Cross Join
        # Get the commerces columns. to add in cross join query
        commerces_columns = [i.split('.')[-1] for i in saf_columns if i.split('.')[-2] == 'commerces']
        if len(commerces_columns) > 1:
            replace_names = {
                'user_id': 'userid',
                'seller_id': 'sellerid',
                'supervisor_id': 'supervisorid'
            }
            commerces = self.query_commerce_categories().rename(columns=replace_names)
            commerces = commerces[commerces_columns]
            df = df.merge(commerces)
        return df

    def sales_per_month(self, from_date, to_date):
        """
        Makes query to get how much of a product is selled per
        month.

        Returns:
            df (Pandas.DataFrame): dataframe with the query results.
        """
        engine = create_engine(self.conn_str)
        sub_query = f""" select orders.userid, orders.productid, orderdt, (quantity * priceperunit) as sales
                        from orders 
                        where orders.customerid = '{self.customer_id}'
                        and orderdt between {from_date} and dateadd(day, -1, '{to_date}') """
        sub_query, entities = self.__parse_joins(sub_query)
        sub_query = self.__parse_query(sub_query, entities=entities)

        with engine.connect() as conn:
            # Query orders
            query = f"""
            with accum_sales as ({sub_query})
            select  accum_sales.userid as user_id, accum_sales.productid as product_id, sum(sales) as sales
            from accum_sales
            group by accum_sales.userid, accum_sales.productid
            """
            df = pd.read_sql(query, conn)

        return df

    def query_daily_metrics(self, from_date, to_date, strategy_id, customer_id, basic_months=None, debug=False):
        print(from_date)
        print(to_date)
        print('strategy', strategy_id)
        print(basic_months)
        print(self.conn_str)
        engine = create_engine(self.conn_str)
        with engine.connect() as conn:
            basic_sku = f"""
                select orders.userid,
                        orders.productid,
                        min(orders.orderdt) as date
                from orders
                join commerces
                on orders.userid = commerces.userid
                where orders.customerid = '{customer_id}'
                    and orderdt >= dateadd('month', -{basic_months}, '{from_date}')
            """
            basic_sku = self.__parse_query(basic_sku, entities=['commerces', 'orders'])
            basic_sku += f"""
                group by orders.userid, orders.productid
            """
            # Order query
            query_1 = f"""
                SELECT count(distinct orders.productid) as n_orders,
                    orders.userid,
                    date(orderdt) as orderdt
                FROM orders 
                JOIN products
                ON products.productid = orders.productid
                JOIN commerces
                on commerces.userid = orders.userid
            """
            # if basic_months:
            #     query_1 += f"""
            #         JOIN ({basic_sku}) first_buy
            #         ON orders.orderdt > first_buy.date
            #             and orders.userid = first_buy.userid
            #             and orders.productid = first_buy.productid
            #     """
            query_1 += f"""
                WHERE orders.customerid = '{customer_id}'
                    AND orderdt between '{from_date}' and '{to_date}'
            """
            query_1 = self.__parse_query(query_1, entities=['commerces', 'orders', 'products'])
            query_1 = query_1 + 'group by orders.userid, date(orderdt)'
            # Suggestion query
            query_2 = f"""
                SELECT count(distinct suggestions.productid) as n_suggestions,
                    suggestions.userid,
                    date(suggestiondt) as suggestiondt
                FROM suggestions
                JOIN commerces
                ON suggestions.userid = commerces.userid
                JOIN products
                ON products.productid = suggestions.productid
                WHERE suggestions.customerid = '{customer_id}'
                    AND suggestions.strategyId = '{strategy_id}'
                    AND suggestiondt between '{from_date}' and '{to_date}'
            """
            query_2 = self.__parse_query(query_2, entities=['commerces', 'products', 'suggestions'])
            query_2 = query_2 + 'group by suggestions.userid, date(suggestiondt)'
            # Intersection query
            query_3 = f"""
                SELECT coalesce(count(distinct suggestions.productid), 0) as n_intersection,
                    suggestions.userid,
                    date(suggestiondt) as suggestiondt
                FROM suggestions
                JOIN commerces
                on commerces.userid = suggestions.userid
                JOIN products
                on products.productid = suggestions.productid
                JOIN orders
                ON orders.productid = suggestions.productid and orders.userid = suggestions.userid and suggestions.suggestiondt = orders.orderdt
                join ({basic_sku}) first_buy
                ON orders.orderdt > first_buy.date
                        and orders.userid = first_buy.userid
                        and orders.productid = first_buy.productid
                WHERE suggestions.customerid = '{customer_id}'
                    AND suggestiondt between '{from_date}' and '{to_date}'
            """
            query_3 = self.__parse_query(query_3, entities=['commerces', 'products', 'orders', 'suggestions'])
            query_3 = query_3 + 'group by suggestions.userid, suggestiondt'
            query = f"""
                SELECT o.orderdt as date,
                o.userid,
                n_suggestions::float,
                n_orders::float,
                coalesce(n_intersection, 0)::float as n_intersection,
                coalesce(n_intersection, 0)::float / n_suggestions as precision,
                coalesce(n_intersection, 0)::float / n_orders as recall
                FROM (
                    -- Query orders
                    {query_1}
                ) o
                JOIN (
                    -- Query suggestions
                    {query_2}
                ) s
                on o.userid = s.userid and o.orderdt = s.suggestiondt
                LEFT OUTER JOIN (
                    -- Query intersections
                    {query_3}
                ) i
                on o.userid = i.userid
                and o.orderdt = i.suggestiondt;
            """
            df = pd.read_sql(query, conn)
            conn.close()
        df.loc[:, 'ratio'] = df['n_suggestions'] / df['n_orders']
        df.loc[:, 'precision'] = df['n_intersection'] / df['n_suggestions']
        df.loc[:, 'recall'] = df['n_intersection'] / df['n_orders']
        df.loc[:, 'f1'] = 2 * df['precision'] * df['recall'] / (df['precision'] + df['recall'])
        df['f1'] = df['f1'].fillna(0.)
        if debug:
            return df
        df = df.groupby(['date'])[['precision', 'recall', 'f1']].mean()
        return df

    
    def query_last_price(self):
        """
        Obtain last price if it was bought previously
        3 queries:
            1.- Obtain last time each product was bought
            2.- Obtain last price 
            3.- All commerces target to get las price.
        Merge all 3 with simple join.

        Return:
            df (pandasDataframe): with userid, productid, orderdt (last time bought), priceperunit (last price)
        """
        engine = create_engine(self.conn_str)
        date_query = f"""
        SELECT userid, productid, MAX(orderdt) as orderdt
        FROM orders
        WHERE customerid = '{self.customer_id}'
        """
        date_query = self.__parse_query(date_query, entities=['orders'])
        date_query += """group by userid, productid"""

        price_query = f"""
        SELECT userid, productid, priceperunit, orderdt
        FROM orders
        WHERE customerid = '{self.customer_id}'
        """
        price_query = self.__parse_query(price_query, entities=['orders'])
        
        commerce_query = f"""
        SELECT *
        FROM commerces
        WHERE customerid = '{self.customer_id}'
        """
        commerce_query = self.__parse_query(commerce_query, entities=['commerces'])
        
        query = f"""
        SELECT dates.userid,
            dates.productid,
            dates.orderdt,
            prices.priceperunit
        FROM ({date_query}) dates
                JOIN ({price_query}) prices
                    ON dates.orderdt = prices.orderdt AND dates.userid = prices.userid AND dates.productid = prices.productid
                JOIN ({commerce_query}) commerces ON commerces.userid = dates.userid
        """
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
