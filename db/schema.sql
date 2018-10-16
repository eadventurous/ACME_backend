CREATE TABLE parcels (
    parcel_id serial PRIMARY KEY,
    weight REAL NOT NULL,
    volume REAL NOT NULL,
    /* TODO: define ENUM of standard shapes */
    shape VARCHAR(100) NOT NULL
);

CREATE TABLE incoming_orders (
    order_id serial PRIMARY KEY,
    created_on TIMESTAMP NOT NULL,
    priority INTEGER NOT NULL,

    parcel_id INTEGER,
    CONSTRAINT incoming_orders_order_id_fkey
        FOREIGN KEY (parcel_id)
        REFERENCES parcels (parcel_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE dispatch_orders (
    incoming_order_id INTEGER PRIMARY KEY,
    CONSTRAINT dispatch_order_incoming_order_id_fkey
        FOREIGN KEY (incoming_order_id)
        REFERENCES incoming_orders (order_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE contacts (
    contact_id serial PRIMARY KEY,
    /*** Fields for general information ***/
    address VARCHAR(255),
    phone_number VARCHAR(20) NOT NULL,
    additional_info TEXT,
    /*** Fields for personal information ***/
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    position VARCHAR(255),
    /*** Fields for company information ***/
    company VARCHAR(255)
);

CREATE TABLE warehouses (
    warehouse_id serial PRIMARY KEY,
    contact_id INTEGER NOT NULL,
    /** Area of warehouse m^2
     */
    max_capacity REAL NOT NULL,
    /** For backward compatibility with old orders
     * in case warehouse shuts down.
     */
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT warehouses_contact_id
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE dispatch_status (
    created_on TIMESTAMP NOT NULL,
    /* TODO: make ENUM of all possible statuses. */
    status VARCHAR(20) NOT NULL,
    warehouse_id INTEGER /* OPTIONAL */,

    dispatch_order_id INTEGER NOT NULL,
    CONSTRAINT dispatch_status_pkey
        PRIMARY KEY (dispatch_order_id, created_on),
    CONSTRAINT dispatch_status_dispatch_order_fkey
        FOREIGN KEY (dispatch_order_id)
        REFERENCES dispatch_orders (incoming_order_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    CONSTRAINT dispatch_status_warehouse_id_fkey
        FOREIGN KEY (warehouse_id)
        REFERENCES warehouses (warehouse_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

/* TODO: Add 'next_vector' parameter. */
CREATE TABLE transportation_vectors (
    vector_id serial PRIMARY KEY,
    weather VARCHAR(50) NOT NULL,
    traffic VARCHAR(255) NOT NULL
);

/* TODO: Fix relation between routes, vectors and operators. */
CREATE TABLE transportation_routes (
    route_id serial PRIMARY KEY,
    transport_type VARCHAR(50) NOT NULL,
    start_location VARCHAR(255) NOT NULL,
    end_location VARCHAR(255) NOT NULL
);

CREATE TABLE delivery_operators (
    operator_id serial PRIMARY KEY,
    contact_id INTEGER NOT NULL,

    CONSTRAINT delivery_operators_contact_id
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE transportation_companies (
    company_id serial PRIMARY KEY,
    contact_id INTEGER NOT NULL,
    /* TODO: Should we create separate table or enum for types? */
    transportation_types VARCHAR(50),

    CONSTRAINT transportation_companies_contact_id_fkey
        FOREIGN KEY (contact_id)
        REFERENCES contacts (contact_id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);
