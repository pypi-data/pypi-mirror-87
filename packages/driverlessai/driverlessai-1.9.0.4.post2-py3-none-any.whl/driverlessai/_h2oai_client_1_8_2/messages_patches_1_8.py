"""messages.py patches for server versions 1.8"""

from .references import *


class ServerObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def dump(self) -> dict:
        d = {k: (v.dump() if hasattr(v, 'dump') else v) for k, v in vars(self).items()}
        return d


# 1.8.0 - 1.8.5.1
class GbqCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class HiveCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class JdbcCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class KdbCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
 

# 1.8.0 - 1.8.6.3
class SnowCreateDatasetArgs(ServerObject):
    def __init__(self, **kwargs) -> None:
        if kwargs.get("sf_user") or kwargs.get("password"):
            raise ValueError(
                "`snowflake_username` and `snowflake_password` are only "
                "supported in Driverless AI server versions >= 1.8.7. "
                "For other Driverless AI server versions, credentials "
                "must be specified in config.toml."
            )
        kwargs.pop("sf_user", None)
        kwargs.pop("password", None)
        super().__init__(**kwargs)


# 1.8
class InterpretParameters(ServerObject):
    """

    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def clone(self) -> 'InterpretParameters':
        return InterpretParameters(self.dai_model, self.dataset, self.target_col, self.prediction_col, self.use_raw_features, self.nfolds, self.klime_cluster_col, self.weight_col, self.drop_cols, self.sample, self.sample_num_rows, self.qbin_cols, self.qbin_count, self.lime_method, self.dt_tree_depth, self.config_overrides, self.vars_to_pdp, self.dia_cols)

    @staticmethod
    def load(d: dict) -> 'InterpretParameters':
        d['dai_model'] = ModelReference.load(d['dai_model'])
        d['dataset'] = DatasetReference.load(d['dataset'])
        return InterpretParameters(**d)


