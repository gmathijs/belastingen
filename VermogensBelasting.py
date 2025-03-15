import sqlite3

class VermogensBelastingCalculator:
    def __init__(self):
        self.conn = sqlite3.connect('mijn_belastingen.db')
        self.cursor = self.conn.cursor()

    def get_vermogensbelasting_schijf(self, asset_value, year, asset_type):
        self.cursor.execute("""
            SELECT lower_limit, upper_limit, tax_rate
            FROM tax_vermogensbelasting
            WHERE year = ? AND asset_type = ? AND lower_limit <= ? AND upper_limit >= ?
        """, (year, asset_type, asset_value, asset_value))
        result = self.cursor.fetchone()
        if result:
            return {
                'lower_limit': result[0],
                'upper_limit': result[1],
                'tax_rate': result[2]
            }
        return None

    def bereken_vermogensbelasting(self, jaar, banktegoed, beleggingen, ontroerendgoed, schulden):
        # Calculate net wealth
        net_vermogen = banktegoed + beleggingen + ontroerendgoed - schulden

        # Calculate tax for each asset type
        belasting_banktegoed = self._bereken_belasting_per_asset(jaar, banktegoed, 'banktegoed')
        belasting_belegingen = self._bereken_belasting_per_asset(jaar, beleggingen, 'beleggingen')
        belasting_ontroerendgoed = self._bereken_belasting_per_asset(jaar, ontroerendgoed, 'ontroerendgoed')

        # Total wealth tax
        totale_belasting = belasting_banktegoed + belasting_belegingen + belasting_ontroerendgoed

        return round(totale_belasting, 2)

    def _bereken_belasting_per_asset(self, year, asset_value, asset_type):
        if asset_value <= 0:
            return 0

        schijf = self.get_vermogensbelasting_schijf(asset_value, year, asset_type)
        if not schijf:
            raise ValueError(f"No tax bracket found for {asset_type} with value {asset_value} in year {year}")

        belasting = asset_value * schijf['tax_rate']
        return belasting

    def close(self):
        self.conn.close()