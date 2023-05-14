prompts_schema = """
请记住数据库的schema名字是BRAZILIAN_ECOMMERCE。9张表的DDL定义如下：
-- olist_customers_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_customers_dataset (
    customer_id VARCHAR(100) COMMENT '客户唯一标识符',
    customer_unique_id VARCHAR(100) COMMENT '客户唯一ID，用于将同一客户的所有记录聚合在一起',
    customer_zip_code_prefix INTEGER COMMENT '客户邮编前缀',
    customer_city VARCHAR(100) COMMENT '客户城市',
    customer_state VARCHAR(100) COMMENT '客户所属州'
);

-- olist_geolocation_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_geolocation_dataset (
    geolocation_zip_code_prefix INTEGER COMMENT '邮编前缀',
    geolocation_lat FLOAT COMMENT '纬度',
    geolocation_lng FLOAT COMMENT '经度',
    geolocation_city VARCHAR(100) COMMENT '城市',
    geolocation_state VARCHAR(100) COMMENT '所属州'
) ;

-- olist_order_items_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_order_items_dataset (
    order_id VARCHAR(100) COMMENT '订单唯一标识符',
    order_item_id INTEGER COMMENT '每个订单中物品的唯一标识符',
    product_id VARCHAR(100) COMMENT '产品唯一标识符',
    seller_id VARCHAR(100) COMMENT '卖家唯一标识符',
    shipping_limit_date TIMESTAMP COMMENT '出货截止日期',
    price FLOAT COMMENT '物品价格',
    freight_value FLOAT COMMENT '运费'
)  ;

-- olist_order_payments_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_order_payments_dataset (
    order_id VARCHAR(100) COMMENT '订单唯一标识符',
    payment_sequential INTEGER COMMENT '每个订单中付款的唯一标识符',
    payment_type VARCHAR(50) COMMENT '付款方式',
    payment_installments INTEGER COMMENT '付款分期数',
    payment_value FLOAT COMMENT '付款金额'
)  ;

-- olist_order_reviews_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_order_reviews_dataset (
    review_id VARCHAR(100) COMMENT '评论唯一标识符',
    order_id VARCHAR(100) COMMENT '订单唯一标识符',
    review_score INTEGER COMMENT '评分（1-5）',
    review_comment_title STRING COMMENT '评论标题',
    review_comment_message STRING COMMENT '评论内容',
    review_creation_date TIMESTAMP COMMENT '评论创建日期',
    review_answer_timestamp TIMESTAMP COMMENT '回答评论的日期和时间'
)  ;

-- olist_orders_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_orders_dataset (
    order_id VARCHAR(100) COMMENT '订单唯一标识符',
    customer_id VARCHAR(100) COMMENT '客户唯一标识符',
    order_status VARCHAR(50) COMMENT '订单状态（字段值包括: delivered, shipped, canceled, invoiced, processing, approved）订单状态（售后，运输，取消，开票，处理，审批完成）',
    order_purchase_timestamp TIMESTAMP COMMENT '订单创建时间',
    order_approved_at TIMESTAMP COMMENT '订单批准时间',
    order_delivered_carrier_date TIMESTAMP COMMENT '运输商交付日期',
    order_delivered_customer_date TIMESTAMP COMMENT '客户交付日期',
    order_estimated_delivery_date TIMESTAMP COMMENT '预计交付日期'
) ;

-- olist_products_dataset table DDL
CREATE TABLE IF NOT EXISTS olist_products_dataset (
  product_id STRING COMMENT '产品ID',
  product_category_name STRING COMMENT '产品类别名称',
  product_name_lenght INT COMMENT '产品名称长度',
  product_description_lenght INT COMMENT '产品描述长度',
  product_photos_qty INT COMMENT '产品照片数量',
  product_weight_g INT COMMENT '产品重量（克）',
  product_length_cm INT COMMENT '产品长度（厘米）',
  product_height_cm INT COMMENT '产品高度（厘米）',
  product_width_cm INT COMMENT '产品宽度（厘米）'
) ;
CREATE TABLE IF NOT EXISTS olist_sellers_dataset (
    seller_id VARCHAR(100) COMMENT '卖家唯一标识符',
    seller_zip_code_prefix INTEGER COMMENT '卖家邮编前缀',
    seller_city VARCHAR(100) COMMENT '卖家城市',
    seller_state VARCHAR(100) COMMENT '卖家所属州'
)  ;
-- product_category_name_translation table DDL
CREATE TABLE IF NOT EXISTS product_category_name_translation (
    product_category_name VARCHAR(100) COMMENT '产品类别名称',
    product_category_name_english VARCHAR(100) COMMENT '产品类别英文翻译'
)  ;
"""

prompts_ord = """
请记住这9张表的实体关系：
1、olist_customers_dataset：客户信息数据集
    实体关系：一个客户可以拥有多个订单，一个订单只能属于一个客户。
    主键：customer_unique_id
    外键：order_id （在“olist_orders_dataset”表中）


2、olist_geolocation_dataset：地理位置信息数据集
    实体关系：一个邮编前缀可以对应多条纬度和经度记录。
    主键：geolocation_zip_code_prefix, geolocation_lat, geolocation_lng
    外键：无

3、olist_order_items_dataset：订单-物品级别数据集
    实体关系：一个订单可以包含多个物品，一个物品只能属于一个订单。
    主键：order_id, order_item_id
    外键：order_id (在“olist_orders_dataset”表中), product_id 和 seller_id (在“olist_products_dataset”和“olist_sellers_dataset”表中)

4、olist_order_payments_dataset：订单支付信息数据集
    实体关系：一个订单可以包含多次付款，一个付款只能属于一个订单。
    主键：order_id, payment_sequential
    外键：order_id (在“olist_orders_dataset”表中)

5、olist_order_reviews_dataset：订单评论数据集
    实体关系：一个订单可以收到多个评论，一个评论只能属于一个订单。
    主键：review_id
    外键：order_id (在“olist_orders_dataset”表中), customer_id (在“olist_customers_dataset”表中)

6、olist_orders_dataset：订单信息数据集
    实体关系：一个订单属于一个客户，一个客户可以拥有多个订单。
    主键：order_id
    外键：customer_id (在“olist_customers_dataset”表中)

7、olist_products_dataset：产品信息数据集
    实体关系：一个产品可以属于一个或多个类别，一个类别可以包含多个产品。
    主键：product_id
    外键：无
8、olist_sellers_dataset：卖家信息数据集
    实体关系：一个卖家可以拥有多个订单，一个订单只能属于一个卖家。
    主键：seller_id
    外键：无

9、product_category_name_translation：产品类别名称翻译数据集
    实体关系：一个原始的产品类别名称可以对应多个英文翻译（可能因语言、时期或使用环境等原因不同）。
    主键：product_category_name
    外键：无
"""
prompts_sql_standard="""
    请你再深入分析下上述DDL和实体关系，会对生成SQL代码有帮助。请记住：接下来我会用业务语言问一些业务问题，我用的数据库叫Clickzetta Lakehouse，
    SQL语言和Spark SQL语言兼容，所以你帮我生成对应的Clickzetta Lakehouse的SQL代码，需要用Spark SQL标准。并请加上中文注释。不要使用use命令。
    在SQL的From语句里带上schema名，格式为from schema.table.
"""
