from math import log10

class PropagationModel:
    """Log distance path loss propagation model to simulate a real environment
    """
    @staticmethod
    def log(distance, tx_power_dbm, frequency, reference_distance=0.2):
        exponent = 3
        reference_loss = 46.6777

        if distance <= reference_distance:
            return tx_power_dbm - reference_loss

        path_loss_db = 10 * exponent * log10 (distance / reference_distance)
        rxc = - reference_loss - path_loss_db

        return tx_power_dbm + rxc
