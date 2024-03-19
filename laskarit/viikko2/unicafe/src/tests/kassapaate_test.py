import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_kassassa_rahaa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassassa_rahaa_oikein_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_lounaita_ei_myyty(self):
        self.assertEqual(self.kassapaate.edulliset+self.kassapaate.maukkaat, 0)

    def test_osta_edullinen_1(self):
        self.kassapaate.syo_edullisesti_kateisella(340)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_osta_edullinen_2(self):
        self.kassapaate.syo_edullisesti_kateisella(340)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_osta_edullinen_3(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(340)
        self.assertEqual(palautus, 100)

    def test_osta_edullinen_maksu_ei_riita_1(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_osta_edullinen_maksu_ei_riita_2(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_osta_edullinen_maksu_ei_riita_3(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(palautus, 200)

    def test_osta_maukas_1(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_osta_maukas_2(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_osta_maukas3(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(palautus, 100)

    def test_osta_maukas_maksu_ei_riita_1(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_osta_maukas_maksu_ei_riita_2(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_osta_maukas_maksu_ei_riita_3(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(palautus, 200)

    def test_osta_edullinen_kortilla_1(self):
        onnistuminen = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(onnistuminen, True)
        self.assertEqual(self.kortti.saldo_euroina(), 7.6)

    def test_osta_edullinen_kortilla_2(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_osta_edullinen_kortilla_3(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_osta_edullinen_kortilla_ei_rahaa(self):
        kortti = Maksukortti(100)
        onnistuminen = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(onnistuminen, False)
        self.assertEqual(kortti.saldo_euroina(), 1.0)
        self.assertEqual(self.kassapaate.edulliset, 0)

    
    def test_osta_maukas_kortilla_1(self):
        onnistuminen = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(onnistuminen, True)
        self.assertEqual(self.kortti.saldo_euroina(), 6.0)

    def test_osta_maukas_kortilla_2(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_osta_maukas_kortilla_3(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_osta_maukas_kortilla_ei_rahaa(self):
        kortti = Maksukortti(100)
        onnistuminen = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(onnistuminen, False)
        self.assertEqual(kortti.saldo_euroina(), 1.0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
        self.assertEqual(self.kortti.saldo_euroina(), 20.0)

    def test_lataa_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kortti.saldo_euroina(), 10.0)
