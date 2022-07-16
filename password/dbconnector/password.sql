DROP TABLE IF EXISTS "service";
CREATE TABLE IF NOT EXISTS "service" (
    "id" UUID NOT NULL PRIMARY KEY,
    "utc_date" TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    "name" TEXT NOT NULL,
    "url" TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "password" BYTEA NOT NULL,
    CONSTRAINT _name_user_uc UNIQUE ("name", "user")
);
