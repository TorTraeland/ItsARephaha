# -*- coding: utf-8 -*-
"""

Playing around with structural reliability
"""

from pyre import *


import time
import datetime
start_time = time.time()


def example_limitstatefunction(X1, X2, X3):
    """
    example limit state function
    """
    return 1 - X2*(1100*X3)**(-1) - (X1*(190*X3)**(-1))**2


# Define a main() function.
def main():

    limit_state = LimitState(example_limitstatefunction)

    # Set some options (optional)
    options = AnalysisOptions()
    # options.printResults(False)

    stochastic_model = StochasticModel()
    # Define random variables
    stochastic_model.addVariable(Lognormal('X1', 500, 100))
    stochastic_model.addVariable(Normal('X2', 2000, 400))
    stochastic_model.addVariable(Uniform('X3', 5, 0.5))

    # If the random variables are correlatet, then define a correlation matrix,
    # else no correlatin matrix is needed
    stochastic_model.setCorrelation(CorrelationMatrix([[1.0, 0.3, 0.2],
                                                       [0.3, 1.0, 0.2],
                                                       [0.2, 0.2, 1.0]]))

    # Perform FORM analysis
#    Analysis = Form(analysis_options=options,
 #                   stochastic_model=stochastic_model, limit_state=limit_state)

    # Perform Distribution analysis
#    Analysis = DistributionAnalysis(
#        analysis_options=options, stochastic_model=stochastic_model, limit_state=limit_state)
    # Perform Crude Monte Carlo Simulation
    Analysis = CrudeMonteCarlo(
        analysis_options=options, stochastic_model=stochastic_model, limit_state=limit_state)

    # Perform Importance Sampling
#    Analysis = ImportanceSampling(
#        analysis_options=options, stochastic_model=stochastic_model, limit_state=limit_state)

    # Some single results:
    beta = Analysis.getBeta()
    failure = Analysis.getFailure()

    print("Beta is {}, corresponding to a failure probability of {}".format(beta, failure))
    run_time = time.time() - start_time
    print(str(datetime.timedelta(seconds=run_time)))

    # This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()