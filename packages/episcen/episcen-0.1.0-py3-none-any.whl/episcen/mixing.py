def force_of_infection(beta_i, mixmat):
    """
    Calculate the force of infection exerted on each population stratum, given
    the force of infection exerted by the infectious individuals in each
    stratum (``beta_i``) and the mixing matrix (``mixmat``).
    """
    return beta_i @ mixmat
