def compute_sensitivity_factor(current_performance: float, target_performance: float, adjustment_cap: float=0.3):
    """
    Function: compute_sensitivity_factor

    Description:
        Calculate sensitivity factor for pacing time series predictions. Time series predictions contain small errors
        which compound over time. This is problematic when attempting to hit specific performance goals. This function
        computes an adjustment factor meant to be an overlaid on top of a time-series forecasted datapoint. This sensitivity
        factor helps adjust data points to make up for previous prediction errors in order to meet a specific performance
        target. The returned sensitivity factor is meant to be multiplied to the predicted datapoint.

    Usage:
        compute_sensitivity_factor( current_performance=0.9,
                                    target_performance=1.0,
                                    adjustment_cap=0.3 )

    Params
        @param current_performance (float) - the current performance. For example if the performance goal is 100% and our model's
        accuracy is currently 90%, then 0.90 should be passed into the current_performance parameter.

        @param target_performance (float) - The desired performance target. From the previous example, if the performance goal is 100%,
        then 1.0 should be passed into the target_performance parameter.

        @param adjustment_cap (float) - caps how much the data point can be adjusted due to pacing. For example, if 0.3 is passed into
        the adjustment_cap parameter, then the value returned from this function with only adjust the predicted data points at
        most 30% up or down.

        @return sensitivity_factor (float)
    """

    #: determine what percentage if the daily spend the adjustment is, and cap it
    sensitivity_factor = 1 + max(min((current_performance - target_performance)/target_performance, adjustment_cap), -1.0 * adjustment_cap)

    return sensitivity_factor

def compute_roi_sensitivity_factor_(revenue: float, cost: float, target_performance: float, units_spent: int, units_left: int, adjustment_cap: float=0.3):
    """
    Function: compute_sensitivity_factor

    Description:
        Calculate sensitivity factor for pacing time series predictions. Time series predictions contain small errors
        which compound over time. This is problematic when attempting to hit specific performance goals. This function
        computes an adjustment factor meant to be an overlaid on top of a time-series forecasted datapoint. This sensitivity
        factor helps adjust data points to make up for previous prediction errors in order to meet a specific performance
        target. The returned sensitivity factor is meant to be multiplied to the predicted datapoint.

        This varient is specifically written for achieving a return on investment performance taget.

    Usage:
        compute_sensitivity_factor_variant( revenue=92.0,
                                            cost=100.0,
                                            target_performance=1.0,
                                            units_spent=10,
                                            units_left=15,
                                            adjustment_cap=0.3 )

    Params

        @param revenue (float): total revenue over the period

        @param cost (float): total cost over the period

        @param target_performance (float): The desired performance target. Example, if 100% then 1.0 should be passed into the parameter.

        @param units_spent (int): Total units spent over the period. Example, if the units is days, this parameter is the current day of the month.

        @param units_left (int): Number of units until the goal needs to be achieved.

        @param adjustment_cap (float): caps how much the data point can be adjusted due to pacing. For example, if 0.3 is passed into
        the adjustment_cap parameter, then the value returned from this function with only adjust the predicted data points at
        most 30% up or down.

        @return sensitivity_factor (float)
    """

    #: calculate the adjustment needed to be made up by the cutoff
    adjustment = revenue / target_performance - cost

    #: calculate the adjustment per day
    adjustment_per_day = adjustment / units_left

    #: calculate average cost per day
    average_cost_per_day = cost / units_spent

    #: determine what percentage if the daily spend the adjustment is, and cap it
    sensitivity_factor = 1 + max(min(adjustment_per_day / average_cost_per_day, adjustment_cap), -1.0 * adjustment_cap)

    return sensitivity_factor