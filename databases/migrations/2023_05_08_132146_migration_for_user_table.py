"""MigrationForUserTable Migration."""

from masoniteorm.migrations import Migration

class MigrationForUserTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table.uuid("id")
            table.enum("sex", ["male", "female"]).nullable()
            table.string('username', 20).unique()
            table.string("email", 128).unique()
            table.string("password", 128).unique()
            table.boolean("is_active", True)
            table.string('first_name', 40).nullable()
            table.string('last_name', 40).nullable()
            table.boolean("is_staff", False)
            table.boolean("is_superuser", False)
            table.boolean("is_verified", False)
            table.datetime("activation_time_expires", nullable=True, now=False)
            table.string('email_code', 14).unique()
            table.string("ip_addr", 20)

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("users")
