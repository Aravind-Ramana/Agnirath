import numpy as np
from scipy.optimize import minimize
import pandas as pd

import config
import state
from constraints import get_bounds, objective, battery_acc_constraint_func, final_battery_constraint_func
from profiles import extract_profiles

def main(route_df):
    segment_array = route_df.iloc[:, 0].to_numpy()
    slope_array = route_df.iloc[:, 2].to_numpy()
    lattitude_array = route_df.iloc[:, 3].to_numpy()
    longitude_array = route_df.iloc[:, 4].to_numpy()

    N_V = len(route_df) + 1
    velocity_profile = np.ones(N_V) * state.InitialGuessVelocity

    bounds = get_bounds(N_V)
    constraints = [
        {
            "type": "ineq",
            "fun": battery_acc_constraint_func,
            "args": (
                segment_array, slope_array, lattitude_array, longitude_array
            )
        },
        {
            "type": "ineq",
            "fun": final_battery_constraint_func,
            "args": (
                segment_array, slope_array, lattitude_array, longitude_array
            )
        },
    ]


    print("Starting Optimisation")
    print("=" * 60)

    optimised_velocity_profile = minimize(
        objective, velocity_profile,
        args=(segment_array,),
        bounds=bounds,
        method=state.ModelMethod,
        constraints=constraints,
        options={
            'verbose': 3,
        }
    )
    optimised_velocity_profile = np.array(optimised_velocity_profile.x)*1

    print("done.")
    print("Total time taken for race:", objective(optimised_velocity_profile, segment_array), "s")

    outdf = pd.DataFrame(
        dict(zip(
            ['CummulativeDistance', 'Velocity', 'Acceleration', 'Battery', 'EnergyConsumption', 'Solar', 'Time'],
            extract_profiles(optimised_velocity_profile, segment_array, slope_array, lattitude_array, longitude_array)
        ))
    )

    return outdf

if __name__ == "__main__":
    outdf = main(state.route_df)
    outdf.to_csv('run_dat.csv', index=False)
    print("Written results to `run_dat.csv`")