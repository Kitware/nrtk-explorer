# Nebari

This directory aim to capture and test nrtk-explorer in the context of a nebari deployment.

## Create conda environment

```
conda env create -f environment.yml
```

## Activate environment

```
conda activate nrtk-explorer
```

## Test application

```
python -m nrtk_explorer.app.main --port 0
```

## Test execution with proxy

```
python -m jhsingle_native_proxy.main --authtype=none --no-force-alive \
    --conda-env=nrtk-explorer \
    python {-}m nrtk_explorer.app.main {--}server {--}host 0.0.0.0 {--}port {port}
```

Then try to connect to `http://localhost:8888/`
