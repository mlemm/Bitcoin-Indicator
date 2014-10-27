#!/usr/bin/env python

#Markus Lemm - 260444 - August 18, 2014
#Bitcoin indicator

import sys
import gtk
import appindicator
import urllib2
import os

#refresh is seconds * 1000 - currently 10 minutes
REFRESH_PRICE = 600000
CURRENCY = "CAD"

class checkBitCoinPrice:
    def __init__(self):
        self.ind = appindicator.Indicator("bitcoin-ticker-indicator", os.path.dirname(os.path.realpath(__file__)) + "/bit.png", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_label(" ", "")
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)


    def menu_setup(self):
        self.menu = gtk.Menu()

        self.sub_menu = gtk.Menu()

        self.currency = gtk.MenuItem("Currency")
        self.currency.show()
        self.menu.append(self.currency)

        #sub menu items
        self.CADcurrency = gtk.MenuItem("Canadian")
        self.CADcurrency.connect("activate", self.change_to_canadian)
        self.CADcurrency.show()
        self.sub_menu.append(self.CADcurrency)

        self.USDcurrency = gtk.MenuItem("US")
        self.USDcurrency.connect("activate", self.change_to_us)
        self.USDcurrency.show()
        self.sub_menu.append(self.USDcurrency)

        self.EURcurrency = gtk.MenuItem("Euro")
        self.EURcurrency.connect("activate", self.change_to_euro)
        self.EURcurrency.show()
        self.sub_menu.append(self.EURcurrency)

        self.GBPcurrency = gtk.MenuItem("British Pound")
        self.GBPcurrency.connect("activate", self.change_to_british)
        self.GBPcurrency.show()
        self.sub_menu.append(self.GBPcurrency)

        #add submenu
        self.currency.set_submenu(self.sub_menu)

        self.refresh = gtk.MenuItem("Refresh")
        self.refresh.connect("activate",self.manual_labelx)
        self.refresh.show()
        self.menu.append(self.refresh)

        self.exit = gtk.MenuItem("Exit")
        self.exit.connect("activate",self.exit_menu)
        self.exit.show()
        self.menu.append(self.exit)


    def exit_menu(self, widget):
        sys.exit(0)

    def change_to_canadian(self, widget):
        global CURRENCY
        CURRENCY = "CAD"
        self.manual_labelx(self)

    def change_to_us(self, widget):
        global CURRENCY
        CURRENCY = "USD"
        self.manual_labelx(self)

    def change_to_euro(self, widget):
        global CURRENCY
        CURRENCY = "EUR"
        self.manual_labelx(self)

    def change_to_british(self, widget):
        global CURRENCY
        CURRENCY = "GBP"
        self.manual_labelx(self)


    def manual_labelx(self, widget):
        req = urllib2.Request('https://api.bitcoinaverage.com/ticker/' + CURRENCY)

        try: #if not able to connect then just output 0.00
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            last_price = "0.00"
        except Exception:
            last_price = "0.00"
        else:
            the_page = response.read().split(",")
            last_price = the_page[3]

        last_price = last_price.replace("\"last\":", "")
        self.ind.set_label("$" + last_price.strip() + " " + CURRENCY)

    
    def change_labelx(self):
        self.manual_labelx(self)
        return True #if set to False will only return once


    def main(self):
        self.change_labelx()
        gtk.timeout_add(REFRESH_PRICE, self.change_labelx)
        gtk.main()


if __name__ == "__main__":
    indicator = checkBitCoinPrice()
    indicator.main()
