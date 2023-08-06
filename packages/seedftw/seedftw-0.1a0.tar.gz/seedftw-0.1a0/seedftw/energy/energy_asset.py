# -*- coding: utf-8 -*-
"""
Functions related to modelling of energy assets.

This file can also be imported as a module and contains the following
functions:

    * wind_turbine_generator - converts wind speed to power output of a wind turbine
    * solar_pv_generator - convert solar irradiance to the power output of a PV installation


References:
    J. Twidell & T. Weir, Renewable Energy Resources, 2nd edition, 
    Taylor and Francis, 2006

"""

# Import all useful libraries
import casadi as ca
import casadi.tools
import numpy as np


def wind_turbine_generator(
    wind_speed,
    rated_power=1000,
    cut_in_wind_speed=5,
    rated_wind_speed=12,
    cut_out_wind_speed=30,
):
    """Models the power production curve of a standard wind turbine.
    The model is based upon (Twidell, 2006), pp. 306-307.

    Parameters
    ----------
    wind_speed : np.array
        Wind speed [m/s]
    rated_power : float
        Rated power of the turbine [W]
        (default: 1000)
    cut_in_wind_speed : float
        Cut-in wind speed of the turbine [m/s]
        (default: 5)
    rated_wind_speed : float
        Rated wind speed of the turbine [m/s]
        (default: 12)
    cut_out_wind_speed : float
        Cut-out wind speed of the turbine [m/s]
        (default: 30)

    Raises
    ------
    None

    Returns
    -------
    power_output : np.array
        Power production corresponding to the values of wind_speed [W]
    """

    k_cubic = np.where(
        (wind_speed >= cut_in_wind_speed) & (wind_speed < rated_wind_speed)
    )
    k_rated = np.where(
        (wind_speed >= rated_wind_speed) & (wind_speed <= cut_out_wind_speed)
    )

    # k_zero = np.where((wind_speed<=cut_in_wind_speed) | (wind_speed>cut_out_wind_speed))
    power_output = np.zeros(np.size(wind_speed))

    u_ci_3 = cut_in_wind_speed ** 3
    u_R_3 = rated_wind_speed ** 3
    a = rated_power / (u_R_3 - u_ci_3)
    b = u_ci_3 / (u_R_3 - u_ci_3)
    power_output[k_cubic,] = (
        a
        * (
            wind_speed[
                k_cubic,
            ]
            ** 3
        )
        - b * rated_power
    )

    power_output[
        k_rated,
    ] = rated_power

    return power_output


def solar_pv_generator(solar_radiation, rated_power=1000, rated_radiation=1000):
    """Models the power production curve of a standard solar PV panel.
    The model is based upon a simplified linear model.

    Parameters
    ----------
    wind_speed : np.array
        Values of the incident radiation on the panel [W/m^2]
    rated_power : float
        Rated power of the inverter of the PV panel [W]
        (default: 1000)
    rated_radiation : float
        Values of the design radiation on the panel [W/m^2]
        (default: 1000)

    Raises
    ------
    None

    Returns
    -------
    power_output : np.array
        Power production corresponding to the values of solar_radiation [W]
    """
    power_output = rated_power * (solar_radiation / rated_radiation)

    # Forcing the output to not exceed the rated power
    k_excess = np.where(power_output > rated_power)
    power_output[
        k_excess,
    ] = rated_power

    return power_output


def battery_optimal_controller(
    price,
    local_demand=None,
    local_production=None,
    initial_soc=0,
    capacity=1e4,
    rated_power=1e3,
    charge_efficiency=0.98,
    discharge_efficiency=0.98,
    transformer_sizing=np.inf,
):

    ## System description
    # State vector
    x = ca.tools.struct_symMX(["SOC"])

    # Input vector
    u = ca.tools.struct_symMX(["Pin", "Pout"])

    # State equations
    dxdt = ca.tools.struct_MX(x)

    dxdt["SOC"] = charge_efficiency * u["Pin"] - u["Pout"] / discharge_efficiency

    # ODE Right-hand side
    rhs = dxdt
    f = ca.Function("f", [x, u], [dxdt], ["x", "u"], ["dx/dt"])

    dt = ca.MX.sym("dt")

    # RK4
    k1 = f(x, u)
    k2 = f(x + dt / 2.0 * k1, u)
    k3 = f(x + dt / 2.0 * k2, u)
    k4 = f(x + dt * k3, u)
    xf = x + dt / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)

    # Single step time propagation
    F_RK4 = ca.Function("F_RK4", [x, u, dt], [xf], ["x[k]", "u[k]", "dt"], ["x[k+1]"])

    ## ----------- Optimal control -------------------
    opti = ca.Opti()

    # Optimization horizon
    N = len(price)
    price = price.reshape(1, N)

    # Decision variables for states and inputs
    X = opti.variable(x.size, N + 1)

    SOC = X[0, :]
    U = opti.variable(u.size, N)

    if local_demand is None and local_production is None:
        y_Pimport = U[0, :]
        y_Pexport = U[1, :]
    else:
        if local_demand is None:
            local_demand4opt = np.zeros(N)
        else:
            local_demand4opt = local_demand

        if local_production is None:
            local_production4opt = np.zeros(N)
        else:
            local_production4opt = local_production

        local_demand4opt = local_demand4opt.reshape(1, N)
        local_production4opt = local_production4opt.reshape(1, N)

        y_Pimport = ca.fmax(
            0, U[0, :] + local_demand4opt - U[1, :] - local_production4opt
        )
        y_Pexport = ca.fmax(
            0, U[1, :] + local_production4opt - U[0, :] - local_demand4opt
        )

    Pin_battery = U[0, :]
    Pout_battery = U[1, :]

    # Initial state is a parameter
    x0 = initial_soc
    opti.subject_to(X[:, 0] == x0)
    opti.subject_to(X[0, :] <= capacity)
    opti.subject_to(X[0, :] >= 0)

    opti.subject_to(U[0, :] <= rated_power)
    opti.subject_to(U[0, :] >= 0)
    opti.subject_to(U[1, :] <= rated_power)
    opti.subject_to(U[1, :] >= 0)

    # State constraints
    for k in range(N):
        opti.subject_to(X[:, k + 1] == F_RK4(X[:, k], U[:, k], 1))

    if np.isinf(transformer_sizing) is False:
        opti.subject_to(y_Pimport <= transformer_sizing)
        opti.subject_to(y_Pexport <= transformer_sizing)

    revenue = -ca.sum2(ca.times(y_Pimport, price)) + ca.sum2(ca.times(y_Pexport, price))
    opti.minimize(-revenue)

    opti.solver("ipopt")
    sol = opti.solve()

    t = np.linspace(1, N, num=N, axis=0)
    val_Pout = sol.value(Pout_battery)
    val_Pin = sol.value(Pin_battery)
    val_SOC = sol.value(SOC)
    val_revenue = sol.value(revenue)
    val_export = sol.value(y_Pexport)
    val_import = sol.value(y_Pimport)

    performance = dict(
        revenue=np.sum(val_revenue),
        energy_output=np.sum(val_Pout),
        energy_intake=np.sum(val_Pin),
        energy_losses=np.sum(val_Pin) - np.sum(val_Pout),
        energy_export=np.sum(val_export),
        energy_import=np.sum(val_import),
    )

    timeseries = dict(
        t=t,
        soc=val_SOC,
        input_power=val_Pin,
        output_power=val_Pout,
        revenue=val_revenue,
        price=price.reshape(N, 1),
        energy_export=val_export,
        energy_import=val_import,
    )

    timeseries["accumulated_revenue"] = np.cumsum(
        np.multiply(
            (timeseries["energy_export"] - timeseries["energy_import"]).reshape(1, N),
            timeseries["price"].reshape(1, N),
        )
    )

    if local_demand is None:
        performance["local_demand"] = np.sum(local_demand)
        timeseries["local_demand"] = local_demand
    if local_production is None:
        performance["local_production"] = np.sum(local_production)
        timeseries["local_production"] = local_production

    return performance, timeseries
