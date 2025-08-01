import ROOT
import numpy as np

def check_lep_origin_pdg_per_event(input_file):
    """
    Reads the lep_origin branch from a ROOT file and checks for each event if
    it contains PDG IDs 23 (at least twice), 24, and -24 in lep_origin.
    Returns a list of 1 (if present) or 0 (if not) for each event.

    Parameters:
    input_file (str): Path to the ROOT file containing the events tree.

    Returns:
    list: List of 1/0 for each event, indicating presence of required PDG IDs.
    """
    # Open ROOT file
    f = ROOT.TFile.Open(input_file)
    if not f or f.IsZombie():
        print("Error: Cannot open input file")
        return []
    tree = f.Get("events")
    if not tree:
        print("Error: Cannot find 'events' tree")
        f.Close()
        return []

    # Initialize results and diagnostics
    results = []
    total_events = 0
    events_with_required_pdgs = 0
    all_pdg_ids = set()

    # Iterate over all events
    for event in tree:
        total_events += 1
        lep_origin = getattr(event, "lep_origin", None)
        if lep_origin is None:
            print(f"Warning: lep_origin branch not found in event {total_events}")
            results.append(0)
            continue

        # Update set of all PDG IDs seen
        all_pdg_ids.update(lep_origin)

        # Count occurrences of each PDG ID in this event
        pdg_counts = {}
        for pdg in lep_origin:
            pdg_counts[pdg] = pdg_counts.get(pdg, 0) + 1

        # Check for required PDG IDs: 23 (at least twice), 24, -24
        if (pdg_counts.get(23, 0) >= 2 and
            pdg_counts.get(24, 0) >= 1 and
            pdg_counts.get(-24, 0) >= 1):
            results.append(1)
            events_with_required_pdgs += 1
            print(f"Event {total_events} has required PDG IDs: {pdg_counts}")
        else:
            results.append(0)

    # Print diagnostics
    print(f"Total events processed: {total_events}")
    print(f"Events with PDG IDs 23 (x2), 24, -24: {events_with_required_pdgs}")
    print(f"All PDG IDs seen: {sorted(all_pdg_ids)}")

    f.Close()
    return results

# Example usage
if __name__ == "__main__":
    input_file = "/eos/user/l/lberiet/ttZ_diff_results/lepton_eff/result/mgp8_pp_ttz_5f_84TeV_ttzlep.root"
    results = check_lep_origin_pdg_per_event(input_file)
    print(f"Per-event results (first 10): {results[:10]}")
    print(f"Number of events with required PDG IDs: {sum(results)}")