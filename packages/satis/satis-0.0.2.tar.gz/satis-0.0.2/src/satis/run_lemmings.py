from satis import (display_header, read_signals, extract_subset, write_output, plot_time_signals,
                       plot_fourier_convergence, plot_psd_convergence, plot_fourier_variability, plot_psd_variability)

filename = "Uref_Probes.dat"
remove_average = False
diagnostic = "fourier_convergence"
discardphase = False
dbspl = False
target_frequency = 560 #2.6
transient_time = 0.0 #0.201
unit = "Unit"
nb_blocks = 1
window_shape = 'flat'
overlap = 0
subset = False

display_header()
TIME, SIGNALS = read_signals(filename, remove_average)

if subset:
    SIGNALS = extract_subset(subset, SIGNALS)

write_output(
    TIME,
    SIGNALS,
    target_frequency,
    transient_time,
    discardphase,
    unit,
    dbspl)

if diagnostic == 'time':
    plot_time_signals(
        TIME,
        SIGNALS,
        target_frequency,
        transient_time,
        unit)
elif diagnostic == 'fourier_convergence':
    plot_fourier_convergence(
        TIME,
        SIGNALS,
        target_frequency,
        transient_time,
        unit)
elif diagnostic == 'psd_convergence':
    plot_psd_convergence(
        TIME,
        SIGNALS,
        target_frequency,
        transient_time,
        discardphase,
        dbspl,
        unit,
        nb_blocks,
        window_shape,
        overlap
    )
elif diagnostic == 'fourier_variability':
    plot_fourier_variability(
        TIME,
        SIGNALS,
        target_frequency,
        transient_time,
        unit)
elif diagnostic == 'psd_variability':
    plot_psd_variability(
        TIME,
        SIGNALS,
        target_frequency,
        transient_time,
        nb_blocks,
        window_shape,
        overlap
    )
