"""MLI module of official Python client for Driverless AI."""

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

from driverlessai import _core
from driverlessai import _experiments
from driverlessai import _utils


class Interpretation(_utils.ServerJob):
    """Interact with a MLI interpretation on the Driverless AI server."""

    def __init__(
        self, client: "_core.Client", key: str, update_method: Callable[[str], Any]
    ) -> None:
        # super() calls _update() which relies on _update_method()
        self._update_method = update_method
        super().__init__(client=client, key=key)
        self._artifacts: Optional[InterpretationArtifacts] = None
        self._experiment: Optional[_experiments.Experiment] = None

    @property
    def artifacts(self) -> "InterpretationArtifacts":
        """Interact with artifacts that are created when the experiment completes."""
        if not self._artifacts:
            self._artifacts = InterpretationArtifacts(
                self._client, self._get_raw_info()
            )
        return self._artifacts

    @property
    def experiment(self) -> Optional[_experiments.Experiment]:
        """Experiment for the interpretation."""
        if not self._experiment:
            try:
                self._experiment = self._client.experiments.get(
                    self._get_raw_info().entity.parameters.dai_model.key
                )
            except self._client._server_module.protocol.RemoteError:
                # assuming a key error means deleted experiment, if not the error
                # will still propagate to the user else where
                self._experiment = None
        return self._experiment

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self.key} {self.name}"

    def __str__(self) -> str:
        return f"{self.name} ({self.key})"

    def _update(self) -> None:
        self._set_raw_info(self._update_method(self.key))
        self._set_name(self._get_raw_info().entity.description)

    def delete(self) -> None:
        """Delete MLI interpretation on Driverless AI server."""
        try:
            self._client._backend.delete_interpretation(self.key)
        except self._client._server_module.protocol.RemoteError as re:
            print(self._client._backend._format_server_error(re.message["message"]))
            return
        print("Driverless AI Server reported interpretation", self, "deleted.")

    def rename(self, name: str) -> "Interpretation":
        """Change interpretation display name.

        Args:
            name: new display name
        """
        self._client._backend.update_mli_description(self.key, name)
        self._update()
        return self

    def result(self, silent: bool = False) -> "Interpretation":
        """Wait for job to complete, then return an Interpretation object."""
        self._wait(silent)
        return self


class InterpretationArtifacts:
    """Interact with files created by a MLI interpretation on the Driverless AI server.
    """

    def __init__(self, client: "_core.Client", info: Any) -> None:
        self._client = client
        self._paths = {
            "log": getattr(info.entity, "log_file_path", ""),
            "lime": getattr(info.entity, "lime_rc_csv_path", ""),
            "shapley_transformed_features": getattr(
                info.entity, "shapley_rc_csv_path", ""
            ),
            "shapley_original_features": getattr(
                info.entity, "shapley_orig_rc_csv_path", ""
            ),
            "python_pipeline": getattr(info.entity, "scoring_package_path", ""),
        }

    def download(
        self,
        only: Union[str, List[str]] = None,
        dst_dir: str = ".",
        overwrite: bool = False,
    ) -> Dict[str, str]:
        """Download interpretation artifacts from the Driverless AI server. Returns
        a dictionary of relative paths for the downloaded artifacts.

        Args:
            only: specify specific artifacts to download, use
                ``interpretation.artifacts.list()`` to see the available
                artifacts on the Driverless AI server
            dst_dir: directory where interpretation artifacts will be saved
            overwrite: overwrite existing files
        """
        dst_paths = {}
        if isinstance(only, str):
            only = [only]
        if only is None:
            only = self.list()
        for k in only:
            path = self._paths.get(k)
            if path:
                dst_paths[k] = self._client._download(
                    server_path=path, dst_dir=dst_dir, overwrite=overwrite
                )
            else:
                print(f"'{k}' does not exist on the Driverless AI server.")
        return dst_paths

    def list(self) -> List[str]:
        """List of interpretation artifacts that exist on the Driverless AI server."""
        return [k for k, v in self._paths.items() if v]


class InterpretationMethods:
    """Methods for retrieving different interpretation types on the
    Driverless AI server."""

    def __init__(
        self,
        client: "_core.Client",
        list_method: Callable[[int, int], Any],
        update_method: Callable[[str], Any],
    ):
        self._client = client
        self._list = list_method
        self._update = update_method

    def get(self, key: str) -> "Interpretation":
        """Get an Interpretation object corresponding to a MLI interpretation
        on the Driverless AI server.

        Args:
            key: Driverless AI server's unique ID for the MLI interpretation
        """
        return Interpretation(self._client, key, self._update)

    def list(
        self, start_index: int = 0, count: int = None
    ) -> Sequence["Interpretation"]:
        """List of Interpretation objects available to the user.

        Args:
            start_index: index on Driverless AI server of first interpretation to list
            count: max number of interpretations to request from the
                Driverless AI server
        """
        if count:
            data = self._list(start_index, count)
        else:
            page_size = 100
            page_position = start_index
            data = []
            while True:
                page = self._list(page_position, page_size)
                data += page
                if len(page) < page_size:
                    break
                page_position += page_size
        return _utils.ServerObjectList(
            data=data, get_method=self.get, item_class_name=Interpretation.__name__
        )


class IIDMethods(InterpretationMethods):
    pass


class TimeseriesMethods(InterpretationMethods):
    pass


class MLI:
    """Interact with MLI interpretations on the Driverless AI server.

    Attributes:
        iid (IIDMethods): retrieve IID interpretations
        timeseries (TimeseriesMethods): retrieve timeseries interpretations
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self.iid = IIDMethods(
            client=client,
            list_method=lambda x, y: client._backend.list_interpretations(x, y).items,
            update_method=client._backend.get_interpretation_job,
        )
        self.timeseries = TimeseriesMethods(
            client=client,
            list_method=client._backend.list_interpret_timeseries,
            update_method=client._backend.get_interpret_timeseries_job,
        )

    def _create_iid_interpretation_async(
        self, experiment: _experiments.Experiment, **kwargs: Any
    ) -> str:
        params = self._client._server_module.InterpretParameters(
            dai_model=self._client._server_module.ModelReference(experiment.key),
            dataset=self._client._server_module.DatasetReference(
                experiment.datasets["train_dataset"].key
            ),
            target_col=experiment.settings["target_column"],
            use_raw_features=kwargs.get("use_raw_features", True),
            prediction_col=kwargs.get("prediction_col", ""),
            weight_col=kwargs.get("weight_col", ""),
            drop_cols=kwargs.get("drop_cols", []),
            klime_cluster_col=kwargs.get("klime_cluster_col", ""),
            nfolds=kwargs.get("nfolds", 3),
            sample=kwargs.get("sample", True),
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            qbin_cols=kwargs.get("qbin_cols", []),
            qbin_count=kwargs.get("qbin_count", 0),
            lime_method=kwargs.get("lime_method", "k-LIME"),
            dt_tree_depth=kwargs.get("dt_tree_depth", 3),
            vars_to_pdp=kwargs.get("vars_to_pdp", 10),
            dia_cols=kwargs.get("dia_cols", []),
            testset=self._client._server_module.DatasetReference(""),
            debug_model_errors=kwargs.get("debug_model_errors", False),
            debug_model_errors_class=kwargs.get("debug_model_errors_class", ""),
            config_overrides=kwargs.get("config_overrides", ""),
        )
        return self._client._backend.run_interpretation(params)

    def _create_timeseries_interpretation_async(
        self, experiment: _experiments.Experiment, **kwargs: Any
    ) -> str:
        test_dataset_key = (
            experiment.datasets["test_dataset"].key
            if experiment.datasets["test_dataset"]
            else ""
        )
        params = self._client._server_module.InterpretParameters(
            dataset=self._client._server_module.ModelReference(""),
            target_col=None,
            use_raw_features=None,
            prediction_col=None,
            weight_col=None,
            drop_cols=None,
            klime_cluster_col=None,
            nfolds=None,
            sample=None,
            qbin_cols=None,
            qbin_count=None,
            lime_method=None,
            dt_tree_depth=None,
            vars_to_pdp=None,
            dia_cols=None,
            debug_model_errors=False,
            debug_model_errors_class="",
            dai_model=self._client._server_module.ModelReference(experiment.key),
            testset=self._client._server_module.DatasetReference(test_dataset_key),
            sample_num_rows=kwargs.get("sample_num_rows", -1),
            config_overrides="",
        )
        return self._client._backend.run_interpret_timeseries(params)

    def create(
        self, experiment: "_experiments.Experiment", name: str = None
    ) -> "Interpretation":
        """Create a MLI interpretation on the Driverless AI server and return
        a Interpretation object corresponding to the created interpretation.

        Args:
            experiment: experiment to interpret
            name: interpretation name on the Driverless AI server
        """
        return self.create_async(experiment, name).result()

    def create_async(
        self, experiment: _experiments.Experiment, name: str = None
    ) -> "Interpretation":
        """Launch creation of a MLI interpretation on the Driverless AI server
        and return an Interpretation object to track the status.

        Args:
            experiment: experiment to interpret
            name: interpretation name on the Driverless AI server
        """
        kwargs = {
            "config_overrides": (
                experiment._get_raw_info().entity.parameters.config_overrides
            )
        }
        is_timeseries = bool(experiment.settings.get("time_column", ""))
        if is_timeseries:
            key = self._create_timeseries_interpretation_async(experiment, **kwargs)
            update_method = self.timeseries._update
        else:
            key = self._create_iid_interpretation_async(experiment, **kwargs)
            update_method = self.iid._update
        interpretation = Interpretation(self._client, key, update_method)
        if name:
            interpretation.rename(name)
        return interpretation

    def gui(self) -> _utils.GUILink:
        """Print full URL for the user's MLI page on Driverless AI server."""
        return _utils.GUILink(
            f"{self._client.server.address}{self._client._gui_sep}interpretations"
        )
