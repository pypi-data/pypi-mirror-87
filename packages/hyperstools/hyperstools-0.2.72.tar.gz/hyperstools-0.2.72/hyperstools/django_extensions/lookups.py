from django.db.models import Lookup
from django.db.models.fields import Field


class NoCase(Lookup):
    lookup_name = "lcontains"
    param_pattern = "%%%s%%"
    prepare_rhs = False

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super().process_lhs(compiler, connection, lhs)
        field_internal_type = self.lhs.output_field.get_internal_type()
        db_type = self.lhs.output_field.db_type(connection=connection)
        lhs_sql = connection.ops.field_cast_sql(db_type, field_internal_type) % lhs_sql
        lhs_sql = (
            connection.ops.lookup_cast(self.lookup_name, field_internal_type) % lhs_sql
        )
        return lhs_sql, list(params)

    def process_rhs(self, qn, connection):
        rhs, params = super().process_rhs(qn, connection)
        if self.rhs_is_direct_value() and params and not self.bilateral_transforms:
            params[0] = self.param_pattern % connection.ops.prep_for_like_query(
                params[0]
            )
        return rhs, params

    def as_sql(self, compiler, connection):
        lhs_sql, params = self.process_lhs(compiler, connection)
        rhs_sql, rhs_params = self.process_rhs(compiler, connection)
        params.extend(rhs_params)
        return "%s like Lower(%s)" % (f"Lower({lhs_sql})", rhs_sql), params
        # lhs, lhs_params = self.process_lhs(compiler, connection)
        # rhs, rhs_params = self.process_rhs(compiler, connection)
        # params = lhs_params + rhs_params
        # params = [f"%\\{param}%" for param in params]
        # return "%s like Lower(%s)" % (f"Lower({lhs})", rhs), params

    @staticmethod
    def register():
        Field.register_lookup(NoCase)
