from experiment_engine import get_experiment, list_experiments


def test_experiment_catalog_is_available():
    experiments = list_experiments()
    assert len(experiments) >= 2
    assert all("variables" in item for item in experiments)


def test_experiment_records_observation():
    experiment = get_experiment("polaridad_agua")
    assert experiment is not None
    assert experiment.report()["completed"] is False
    experiment.record_observation("H2O resulta angular.")
    report = experiment.report()
    assert report["completed"] is True
    assert report["observations"] == ["H2O resulta angular."]
