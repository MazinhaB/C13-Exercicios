def sintonia_chr(k, tau, theta):
    """
    Calcula os parâmetros PID pelo método CHR sem sobrevalor
    """

    kp = (0.6 * tau) / (k * theta)
    ti = tau
    td = theta / 2

    return kp, ti, td

def sintonia_cohen_coon(k, tau, theta):
    """
    Calcula os parâmetros PID pelo método Cohe-Coon
    """
    kp = (tau / (k * theta)) * ((16 * tau + 3 * theta) / (12 * tau))
    ti = theta * ((32 + 6 * theta / tau) / (13 + 8 * theta / tau))
    td = (4 * theta) / (11 + 2 * theta / tau)

    return kp, ti, td