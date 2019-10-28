store ="""
CREATE TABLE IF NOT EXISTS store (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Store VARCHAR(30) NOT NULL UNIQUE
)
ENGINE=INNODB;"""
category = """
CREATE TABLE IF NOT EXISTS category (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Category VARCHAR(30) NOT NULL UNIQUE
)
ENGINE=INNODB;"""

product= """
CREATE TABLE IF NOT EXISTS product (
    productid BIGINT NOT NULL PRIMARY KEY,
    productname TEXT NOT NULL,
    category TINYINT UNSIGNED NOT NULL,
    link TEXT NOT NULL,
    description TEXT,
    nutriscore CHAR(1) NOT NULL,
    CONSTRAINT fk_product_category
      FOREIGN KEY (category)
      REFERENCES category(id)
)
ENGINE=INNODB;"""

storeproduct= """
CREATE TABLE IF NOT EXISTS storeproduct (
    productid BIGINT NOT NULL,
    store SMALLINT UNSIGNED NOT NULL,
    CONSTRAINT fk_product_idstore
      FOREIGN KEY (productid)
      REFERENCES product(productid),
    CONSTRAINT fk_idstore_store
      FOREIGN KEY (store)
      REFERENCES store(id)
)
ENGINE=INNODB;"""

productsaved="""
CREATE TABLE IF NOT EXISTS productsaved (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    productid BIGINT NOT NULL,
    subproductid BIGINT NOT NULL,
    CONSTRAINT fk_saved_productid
      FOREIGN KEY (productid)
      REFERENCES product(productid),
    CONSTRAINT fk_saved_subproductid
      FOREIGN KEY (subproductid)
      REFERENCES product(productid)
)
ENGINE=INNODB;"""
