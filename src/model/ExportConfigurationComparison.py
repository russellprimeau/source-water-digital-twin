"""
ExportConfigurationComparison.py

Publish the model definitions behind the model-configuration comparison, so that the
runs summarised in data/configuration_comparison/calibration.csv can be inspected and re-run rather than
only read about.

Local extraction: append --extract, naming the run tree with --runs-dir (or
D3DFM_RUNS).
    Writes data/configuration_comparison/mdu/, mesh/lowres_net.nc and README.md.

No model execution or forcing generation is performed. Model output is not
published: it runs to tens of gigabytes, and the repository distributes model
configuration only.

What is written:

    <run>.mdu           the resolved model definition D-Flow FM echoes into its
                        .dia at startup, which is the configuration as the
                        kernel actually ran it rather than as it was written
    mesh/lowres_net.nc  the coarser of the two horizontal meshes, rebuilt from
                        a run's map output. The finer one is published beside the
                        forcing, as input/FlowFM_net.nc
    README.md           which definition belongs to which row of calibration.csv

The forcing these definitions reference is published with them, under
data/configuration_comparison/input/. It is this comparison's own forcing and not
the thermal simulation's: the two differ in period and in value, the discharge,
meteorological, wind and rainfall series are distinct files, and this set carries a
water-level and a tracer boundary the thermal configuration does not. Neither set
substitutes for the other, and the two horizontal meshes are distinct files too.
"""
from pathlib import Path
import argparse
import io
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
import external_runs                           # noqa: E402
from BuildCalibrationTable import (            # noqa: E402
    ROOT, DATASET_DIR, COMPARISON_DIR, ARCHIVE_SUBDIR, archive_runs,
    committed_table, describe, read_dia)

PUBLISHED_NET = ROOT / 'data/thermal_simulation/input/FlowFM_net.nc'
LOWRES_SOURCE = 'FlowFM_map.nc'

# Every variable the published grid carries, in its order.
NET_VARIABLES = (
    'wgs84', 'mesh2d', 'mesh2d_node_x', 'mesh2d_node_y', 'mesh2d_node_z',
    'mesh2d_edge_x', 'mesh2d_edge_y', 'mesh2d_edge_nodes', 'mesh2d_face_nodes',
    'mesh2d_edge_faces', 'mesh2d_face_x', 'mesh2d_face_y',
    'mesh2d_face_x_bnd', 'mesh2d_face_y_bnd',
)


def export_mdu(runs, out_dir):
    """One .mdu per retained run, taken from the solver's own echo."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for key in sorted(runs):
        block, _ = read_dia(runs[key] / 'FlowFM.dia')
        name = key.replace('/', '_') + '.mdu'
        io.open(out_dir / name, 'w', encoding='utf-8', newline='\n').write(
            chr(10).join(block).rstrip() + chr(10))
        written.append((key, name, len(block)))
    print('wrote %d model definitions' % len(written))
    return written


def export_lowres_grid(runs, out_path):
    """Rebuild the coarse mesh from a run's map output, in the published schema."""
    import netCDF4

    source = None
    for key in sorted(runs):
        candidate = runs[key] / LOWRES_SOURCE
        if not candidate.is_file():
            continue
        ds = netCDF4.Dataset(str(candidate))
        n = len(ds.dimensions.get('mesh2d_nFaces', []))
        ds.close()
        if n == 2603:
            source = candidate
            break
    if source is None:
        raise RuntimeError('no run carries the 2,603-face mesh')

    template = netCDF4.Dataset(str(PUBLISHED_NET))
    src = netCDF4.Dataset(str(source))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dst = netCDF4.Dataset(str(out_path), 'w', format='NETCDF3_CLASSIC')

    for key in template.ncattrs():
        dst.setncattr(key, template.getncattr(key))
    dst.setncattr('history', 'Rebuilt from %s by %s'
                  % (LOWRES_SOURCE, Path(__file__).name))

    sizes = {
        'Two': 2,
        'mesh2d_nNodes': len(src.dimensions['mesh2d_nNodes']),
        'mesh2d_nEdges': len(src.dimensions['mesh2d_nEdges']),
        'mesh2d_nFaces': len(src.dimensions['mesh2d_nFaces']),
        'mesh2d_nMax_face_nodes': len(src.dimensions['mesh2d_nMax_face_nodes']),
    }
    for name, size in sizes.items():
        dst.createDimension(name, size)

    missing = []
    for name in NET_VARIABLES:
        proto = template.variables[name]
        if name not in src.variables and proto.dimensions:
            missing.append(name)
            continue
        fill = proto.getncattr('_FillValue') if '_FillValue' in proto.ncattrs() else None
        var = dst.createVariable(name, proto.dtype, proto.dimensions, fill_value=fill)
        for attr in proto.ncattrs():
            if attr != '_FillValue':
                var.setncattr(attr, proto.getncattr(attr))
        if not proto.dimensions:                      # wgs84, mesh2d: metadata only
            var[...] = proto[...]
        else:
            var[...] = src.variables[name][...]

    dst.close()
    src.close()
    template.close()
    if missing:
        print('   absent from the map output, not written: %s' % ', '.join(missing))
    print('wrote %s from %s' % (out_path.name, source.parent.name))
    return sizes


def export_readme(written, runs, sizes, out_path):
    """Which definition belongs to which row, and which grid each one uses."""
    table = committed_table()
    by_run = dict((r['run'], r) for _, r in table.iterrows())
    lines = [
        '# Model-configuration comparison',
        '',
        '24 run records representing 21 distinct configurations, used in Figure 6 and',
        'Table A3. Configuration settings are recorded in `calibration.csv` and the model',
        'definitions.',
        '',
        '| File or directory | Contents |',
        '| --- | --- |',
        '| `calibration.csv` | One row per run, with settings, comparison statistics, and computational cost. Semicolon-delimited. |',
        '| `mdu/` | Resolved model definitions recorded by D-Flow FM at startup. |',
        '| `input/` | Forcing and boundary conditions for this comparison. |',
        '| `mesh/lowres_net.nc` | Coarse mesh reconstructed from solver output. |',
        '',
        'These forcing files differ from the [thermal simulation inputs](../thermal_simulation/README.md)',
        'and should be used with the comparison models.',
        '',
        'From the repository root:',
        '',
        '```sh',
        'python src/model/CSVplotter.py',
        'python src/model/BuildCalibrationTable.py',
        '```',
        '',
        'These commands write Figure 6 and the Table A3 fragment to `output/`.',
        '[ExportConfigurationComparison.py](../../src/model/ExportConfigurationComparison.py)',
        'regenerates the model definitions, coarse mesh, and this README with',
        '`--extract --runs-dir PATH`. This requires the external solver archive; see',
        '[Materials not published](../../README.md#materials-not-published).',
        '',
        '## Model and mesh mapping',
        '',
        'The resolved definitions all name their grid `flowfm_net.nc`. Use the mesh listed',
        'for each run below:',
        '',
        '- `fine`: `input/FlowFM_net.nc` (4,935 faces).',
        '- `coarse`: `mesh/lowres_net.nc` (2,603 faces).',
        '',
        'When preparing a run directory, set `NetFile` to the corresponding mesh path,',
        'including the correct filename case on case-sensitive filesystems.',
        '',
        '| Model definition | Label in calibration.csv | Mesh |',
        '| --- | --- | --- |',
    ]
    for key, name, _ in written:
        row = by_run.get(key)
        got = describe(runs[key])
        lines.append('| `%s` | %s | %s |' % (
            name,
            (row['Label'].strip() if row is not None else ''),
            'fine' if got['2D Cells'] == 4935 else 'coarse'))
    lines.append('')
    io.open(out_path, 'w', encoding='utf-8', newline='\n').write(chr(10).join(lines))
    print('wrote %s' % out_path.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--extract', action='store_true',
                    help='read the run archive, which is not in this repository')
    ap.add_argument('--runs-dir', help='the solver run tree --extract reads')
    args = ap.parse_args()
    if not args.extract:
        print('Nothing to do without --extract; the published files are already in '
              '%s' % COMPARISON_DIR)
        return 0

    runs = archive_runs(external_runs.resolve(args.runs_dir) / ARCHIVE_SUBDIR)
    written = export_mdu(runs, COMPARISON_DIR)
    sizes = export_lowres_grid(runs, DATASET_DIR / 'mesh' / 'lowres_net.nc')
    export_readme(written, runs, sizes, DATASET_DIR / 'README.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
