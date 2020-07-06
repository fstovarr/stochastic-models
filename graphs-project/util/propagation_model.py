class PropagationModel:
    def log_propagation(t, t1, txPowerDbm=50):
        m_frequency = 9e8
        m_referenceDistance = 0.2
        m_exponent = 3
        m_referenceLoss=46.6777

        distance = GraphHelper.calc_distance(t, t1)

        if distance <= m_referenceDistance:
            return [distance, txPowerDbm - m_referenceLoss]

        pathLossDb = 10 * m_exponent * log10 (distance / m_referenceDistance)
        rxc = -m_referenceLoss - pathLossDb

        return [distance, txPowerDbm + rxc]