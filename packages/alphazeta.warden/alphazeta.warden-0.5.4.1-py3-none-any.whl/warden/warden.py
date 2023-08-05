import json
import os
import csv
import socket
import pandas as pd
import numpy as np
import glob
import logging
import configparser

from datetime import datetime, timedelta
from flask import flash, current_app, has_request_context
from pathlib import Path

from warden_pricing_engine import (get_price_ondate, fx_price_ondate,
                                   multiple_price_grab, price_data_rt,
                                   price_data_fx, price_data_rt_full,
                                   price_data, fx_rate, fxsymbol)
from warden_decorators import MWT, timing
from config import Config

try:
    from cryptoadvance.specter.specter import Specter
    from cryptoadvance.specter.config import DATA_FOLDER
except Exception:
    print("Specter Libraries could not be imported...")
    print("Will search other paths...")


# Returns the current application path
def current_path():
    application_path = os.path.dirname(os.path.abspath(__file__))
    return (application_path)


# Start background threads
# Get Specter tx data and updates every 30 seconds (see config.py)
def background_jobs():
    current_app.specter = specter_update(load=False)
    current_app.services = check_services(load=False)
    # Reload config
    config_file = Config.config_file
    config_settings = configparser.ConfigParser()
    config_settings.read(config_file)
    current_app.settings = config_settings
    current_app.fx = fxsymbol(config_settings['PORTFOLIO']['base_fx'], 'all')
    # Regenerare_nav
    from warden import regenerate_nav
    regenerate_nav()
    return (current_app)


def specter_update(load=True, data_folder=None, idx=0):
    if load:
        with current_app.app_context():
            data = current_app.specter
        return (data)
    if not data_folder:
        with current_app.app_context():
            data_folder = current_app.settings['SPECTER']['specter_datafolder']
    specter_data = Specter(data_folder=data_folder)
    logging.info(f"Finished Building Specter Class from data_folder: {data_folder}")

    return(specter_data)


def specter_update_off(load=True, data_folder=None, idx=0):
    if load:
        with current_app.app_context():
            data = current_app.specter
        return (data)

    if not data_folder:
        with current_app.app_context():
            data_folder = current_app.settings['SPECTER']['specter_datafolder']

    specter_data = Specter(data_folder=data_folder)

    specter_config = specter_data.is_running
    logging.info(f"Finished Building Specter Class from data_folder: {data_folder}")
    logging.info(f"Specter Running: {specter_config}")

    return_dict = {
        'specter_config': specter_config,
        'data_folder': specter_data.data_folder,
        'file_config': specter_data.file_config,
        'config': specter_data.config,
        'is_checking': specter_data.is_checking,
        'is_configured': specter_data._is_configured,
        'is_running': specter_data._is_running,
        'info': specter_data._info,
        'network_info': specter_data._network_info,
        'device_manager_datafolder': specter_data.device_manager.data_folder,
        'last_update': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }

    return_dict['devices'] = {}

    # Parse Devices
    for device in specter_data.device_manager.devices:
        return_dict['devices'][device] = {
            'name':
            specter_data.device_manager.devices[device].__dict__['name'],
            'alias':
            specter_data.device_manager.devices[device].__dict__['alias'],
            'file':
            specter_data.device_manager.devices[device].__dict__['fullpath'],
        }
        logging.info(f"\u001b[32mSuccess, Device {device} imported...\u001b[0m")

    return_dict['wallets'] = {
        'data_folder': specter_data.wallet_manager.working_folder,
        'is_loading': specter_data.wallet_manager.is_loading,
        'wallets': {}
    }
    # Parse Wallets
    for wallet in specter_data.wallet_manager.wallets:
        specter_data.check()
        wallet = specter_data.wallet_manager.wallets[wallet]
        wallet.get_info()
        # is this scanning?
        scan = wallet.rescan_progress

        if not scan:
            logging.info(f"Wallet {wallet} --- looking for txs")
            # Merge list of lists into one single list
            validate_merkle_proofs = specter_data.config['validate_merkle_proofs']
            tx_data = []
            idx_l = idx
            while tx_get != []:
                tx_get = wallet.txlist(idx_l, validate_merkle_proofs=validate_merkle_proofs)
                tx_data.append(tx_get)
                idx_l += 1

            logging.info(f"Wallet {wallet} --- Finished txs")
        else:
            tx_data = []
            logging.warn(f"\u001b[33mWallet {wallet} being scanned {scan}\u001b[0m")

        return_dict['wallets']['wallets'][wallet.__dict__['alias']] = tx_data

    return (return_dict)


# ------------------------------------
# Address and Port checker - to check
# which services are running
def check_server(address, port, timeout=10):
    # Create a TCP socket
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((address, port))
        return True
    except socket.error:
        return False
    finally:
        s.close()


# Check which services are running
# load = True   Forcer json load
# expiry = only loads json if data is not stale by more than n seconds
def check_services(load=True, expiry=60):
    if load:
        try:
            data = current_app.services
            update_time = datetime.strptime(data['last_update'],
                                            "%m/%d/%Y, %H:%M:%S")
            elapsed = (datetime.now() - update_time).total_seconds()
            if expiry:
                if elapsed < expiry:
                    return (data)
            else:
                return (data)
        except Exception as e:
            pass

    services = {}
    services['mynode'] = {
        'name': 'MyNode Server',
        # The below is a list in format [(address, port)] - include as many as needed
        'typical_connections': [('mynode.local', 80), ('127.0.0.1', 80)],
        'running': False,
        'connection': None
    }

    pip_installed = True

    services['specter'] = {
        'name':
        'Specter Server',
        # The below is a list in format [(address, port)] - include as many as needed
        'typical_connections': [('mynode.local', 25441), ('127.0.0.1', 25441),
                                ('localhost', 25441)],
        'running':
        False,
        'connection':
        None
    }
    # Test Connections
    for service in services:
        running = False
        for connection in services[service]['typical_connections']:
            running = check_server(*connection)
            if running:
                services[service]['running'] = True
                services[service]['connection'] = connection
                break

    # Test if specter is running in this machine or remote
    if services['specter']['running']:
        connection = (get_local_ip(), 25441)
        services['specter']['running_on_same_machine'] = check_server(
            *connection)
        # Try again on localhost
        if not services['specter']['running_on_same_machine']:
            connection = ('localhost', 25441)
            services['specter']['running_on_same_machine'] = check_server(
                *connection)

    services['last_update'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if has_request_context:
        current_app.services = services

    return (services)


# Gets local IP Address
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    local_ip_address = s.getsockname()[0]
    return (local_ip_address)

# End Config Variables ------------------------------------------------


def list_specter_wallets(load=True):
    specter_data = specter_update(load)
    return(specter_data.wallet_manager.wallets_names)


# Get all transactions of specific wallet by using alias
@ MWT(timeout=60)
def get_specter_tx(wallet, sort_by='time', idx=0):
    df = pd.DataFrame()
    specter_data = specter_update(load=True)
    specter_data.check()
    wallet = specter_data.wallet_manager.wallets[wallet]
    wallet.get_info()
    # is this scanning?
    scan = wallet.rescan_progress

    if not scan:
        logging.info(f"Wallet {wallet} --- looking for txs")
        tx_data = [
            wallet.txlist(idx)
            for idx in range(0, idx + 1)
        ]
        logging.info(f"Wallet {wallet} --- Finished txs")
        # Merge list of lists into one single list
        validate_merkle_proofs = specter_data.config['validate_merkle_proofs']
        tx_data = wallet.txlist(idx, validate_merkle_proofs=validate_merkle_proofs)
    else:
        tx_data = []
        logging.warn(f"\u001b[33mWallet {wallet} being scanned {scan}\u001b[0m")

    df = df.append(tx_data, ignore_index=True)

    # Sort df
    if not df.empty:
        df = df.sort_values(by=[sort_by], ascending=False)
    return (df)


# This returns all the important metadata to create the Warden Status Page
def warden_metadata():
    specter_data = specter_update(load=True)
    meta = {}
    meta['wallet_list'] = list_specter_wallets()

    # Check if there are specter wallet files, if not do not enable WARden
    if len(meta['wallet_list']) == 0:
        meta['warden_enabled'] = False
        return (meta)
    else:
        meta['warden_enabled'] = True

    meta['wallet_info'] = list_specter_wallets()

    meta['txs'] = {}
    for name in meta['wallet_info']:
        # Line below throws an error when specter is not loaded yet
        meta['txs'][name] = get_specter_tx(name)

    meta['full_df'] = specter_df()

    meta['node_info'] = {
        'info': specter_data.info,
        'network_info': specter_data.network_info
    }

    # Load pickle with previous checkpoint df
    df_pkl = os.path.join(current_path(), 'static/json_files/txs_pf.pkl')
    try:
        meta['df_old'] = pd.read_pickle(df_pkl)
    except IOError:
        meta['df_old'] = None

    # load difference / changes in addresses from file
    ack_file = os.path.join(current_path(), 'static/json_files/txs_ack.json')
    meta['old_new_df_old'] = None
    meta['old_new_df_new'] = None
    try:
        with open(ack_file) as data_file:
            meta['ack_file'] = json.loads(data_file.read())
            # Make a list of missing transactions by id and added transactions by id
            if ('deleted' in meta['ack_file']) or (
                    'added' in meta['ack_file']):
                df_old = meta['df_old']
                df_old['old_new'] = 'old'
                df_new = meta['full_df']
                df_new['old_new'] = 'new'
                # merge two df
                df_merge = pd.concat([df_old, df_new])
                df_merge = df_merge.reset_index(drop=True)
                # Group by TxID
                df_gpby = df_merge.groupby(['txid', 'amount'])
                # Get index of all unique records
                idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
                # Reindex / Filter
                df_merge = df_merge.reindex(idx)
                meta['old_new_df_old'] = df_merge.loc[df_merge['old_new'] ==
                                                      'old']
                meta['old_new_df_new'] = df_merge.loc[df_merge['old_new'] ==
                                                      'new']

    except IOError:
        meta['ack_file'] = None

    return (meta)


# Transactions Engine --------------------------------------
class Trades():
    def __init__(self):
        self.id = None
        self.user_id = "mynode"
        self.trade_inputon = None
        self.trade_date = None
        self.trade_currency = FX
        self.trade_asset_ticker = None
        self.trade_account = None
        self.trade_quantity = None
        self.trade_operation = None
        self.trade_price = None
        self.trade_fees = None
        self.trade_notes = None
        self.trade_reference_id = None
        self.trade_blockchain_id = None
        self.cash_value = None

    def to_dict(self):
        return (vars(self))


@ MWT(timeout=60)
def specter_df(save_files=False, sort_by='trade_date', idx=0):
    specter_data = specter_update(load=True)
    validate_merkle_proofs = specter_data.config['validate_merkle_proofs']
    df = pd.DataFrame()
    idx_l = idx
    tx_list = []
    # Get all txs under every idx
    tx_a = specter_data.wallet_manager.full_txlist(idx_l, validate_merkle_proofs)
    while tx_a != []:
        tx_a = specter_data.wallet_manager.full_txlist(idx_l, validate_merkle_proofs)
        df = df.append(tx_a)
        idx_l += 1

    # Check if txs exists
    if df.empty:
        return df

    # Clean Date String
    df['trade_date'] = pd.to_datetime(df['time'], unit='s')

    # Add additional columns
    df['trade_blockchain_id'] = df['txid']

    # Could include blockchain fees later here
    df['trade_fees'] = int(0)
    df['trade_account'] = df['wallet_alias']
    df['trade_currency'] = current_app.settings['PORTFOLIO']['base_fx']
    df['trade_asset_ticker'] = "BTC"
    df['trade_quantity'] = df['amount']
    df['trade_notes'] = 'Imported from Specter Wallet using MyNode'
    df['trade_reference_id'] = ""

    def trade_operation(value):
        # Get Bitcoin price on each Date
        try:
            if value == 'receive':
                return ("B")
            if value == 'send':
                return ("S")
        except Exception:
            return ("")

    df['trade_operation'] = df['category'].apply(trade_operation)

    df['date_str'] = df['trade_date'].dt.strftime('%Y-%m-%d')

    def btc_price(date_input):
        get_date = datetime.strptime(date_input, "%Y-%m-%d")
        # Create price object
        try:
            fx = fx_price_ondate("USD", current_app.fx['code'], get_date)
            price = (get_price_ondate("BTC", get_date).close) * fx
        except Exception as e:
            price = "Not Found. Error: " + str(e)
        return (price)

    df['trade_price'] = df['date_str'].apply(btc_price)

    df['trade_multiplier'] = 0
    df.loc[df.trade_operation == 'B', 'trade_multiplier'] = 1
    df.loc[df.trade_operation == 'S', 'trade_multiplier'] = -1

    try:
        df['cash_value'] = df['trade_price'] * df['trade_quantity'] * df[
            'trade_multiplier']
    except Exception:
        df['cash_value'] = 0

    # Hash the Pandas df for quick comparison for changes
    from pandas.util import hash_pandas_object
    df['checksum'] = (df['trade_blockchain_id'].astype(str) +
                      df['trade_quantity'].astype(str))
    df['checksum'] = hash_pandas_object(df['checksum'])
    # Every time this function runs, it will save a checksum and full df
    # This is used to make a quick check if there were changes
    # If there are changes, a notification method is started to alert user

    # TEST LINE ------------- Make this a new transaction forced into df
    tester = {
        'trade_date': datetime.now(),
        'trade_currency': 'USD',
        'trade_fees': 0,
        'trade_quantity': 2,
        'trade_multiplier': 1,
        'trade_price': 10000,
        'trade_asset_ticker': 'BTC',
        'trade_operation': 'B',
        'checksum': (5 * (10**19)),
        'txid': 'test',
        'address': 'test_address',
        'amount': 2,
        'status': 'Test_line',
        'trade_account': 'trezor'
    }
    # Comment / Uncomment code below for testing of including new transactions
    # Remove last 2 transactions here
    # df.drop(df.tail(2).index, inplace=True)
    # add transaction above
    # df = df.append(tester, ignore_index=True)

    # END TEST LINE ----------------------------------------------------

    # Files ----------------------------------
    checksum_file = os.path.join(current_path(),
                                 'static/json_files/txs_checksum.json')
    ack_file = os.path.join(current_path(), 'static/json_files/txs_ack.json')
    df_pkl = os.path.join(current_path(), 'static/json_files/txs_pf.pkl')
    # -----------------------------------------

    # Create checksum
    rows_hash = df['checksum'].tolist()
    all_hash = sum(rows_hash)

    try:
        # Loads the all_hash file - first check
        with open(checksum_file) as data_file:
            json_all = json.loads(data_file.read())
            json_all_hash = sum(json_all)
            data_file.close()

        if json_all_hash != all_hash:
            # Let's find which checksums are different and compile a list - save this list
            # so it can be used on main page to highlight changes
            with open(checksum_file) as data_file:
                old_list = json.loads(data_file.read())
                data_file.close()
            new_list = rows_hash

            # find differences
            # force int on both
            old_list = [int(n) for n in old_list]
            new_list = [int(n) for n in new_list]
            deleted_addresses = list(set(old_list).difference(new_list))
            added_addresses = list(set(new_list).difference(old_list))

            # Save these to a file
            json_save = {
                'changes_detected_on':
                datetime.now().strftime("%I:%M %p on %B %d, %Y"),
                'deleted':
                deleted_addresses,
                'added':
                added_addresses
            }

            with open(ack_file, 'w') as fp:
                json.dump(json_save, fp)

    except Exception:
        # Files not found - let's save a new checkpoint
        save_files = True

    # Sort
    df = df.sort_values(by=[sort_by], ascending=False)

    # If Balance change is acknowledge, reset by saving the files

    # Acknowledge list is reduced in a separate function that acknowledges address changes
    if save_files:
        # saves to json and pickle files
        with open(checksum_file, 'w') as fp:
            json.dump(rows_hash, fp)

        with open(ack_file, 'w') as fp:
            json.dump('', fp)

        df.to_pickle(df_pkl)

    return (df)


def find_fx(row, fx=None):
    # row.name is the date being passed
    # row['trade_currency'] is the base fx (the one where the trade was included)
    # Create an instance of PriceData:
    price = fx_price_ondate(current_app.settings['PORTFOLIO']['base_fx'], row['trade_currency'], row.name)
    return price


def transactions_fx():
    # Gets the transaction table and fills with fx information
    # Note that it uses the currency exchange for the date of transaction
    # Get all transactions from Specter and format

    df = specter_df()
    if df.empty:
        return df

    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df = df.set_index('trade_date')
    # Ignore times in df to merge - keep only dates
    df.index = df.index.floor('d')
    df.index.rename('date', inplace=True)
    # The current fx needs no conversion, set to 1
    df[fx_rate()['fx_rate']] = 1
    # Need to get currencies into the df in order to normalize
    # let's load a list of currencies needed and merge
    list_of_fx = df.trade_currency.unique().tolist()
    # loop through currency list
    for currency in list_of_fx:
        if currency == fx_rate()['fx_rate']:
            continue
        # Make a price request
        df[currency] = df.apply(find_fx, axis=1)
    # Now create a cash value in the preferred currency terms
    df['fx'] = df.apply(lambda x: x[x['trade_currency']], axis=1)
    df['cash_value_fx'] = df['cash_value'].astype(float) / df['fx'].astype(
        float)
    df['trade_fees_fx'] = df['trade_fees'].astype(float) / df['fx'].astype(
        float)
    df['trade_price_fx'] = df['trade_price'].astype(float) / df['fx'].astype(
        float)
    return (df)


# UTILS -----------------------------------


def cleancsv(text):  # Function to clean CSV fields - leave only digits and .
    if text is None:
        return (0)
    acceptable = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    str = ""
    for char in text:
        if char in acceptable:
            str = str + char
    str = float(str)
    return (str)


def cleandate(text):  # Function to clean Date fields
    if text is None:
        return (None)
    text = str(text)
    acceptable = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "/", "-", ":",
        " "
    ]
    str_parse = ""
    for char in text:
        if char in acceptable:
            char = '-' if (char == '.' or char == '/') else char
            str_parse = str_parse + char
    from dateutil import parser

    str_parse = parser.parse(str_parse, dayfirst=True)
    return (str_parse)


# PORTFOLIO UTILITIES


@ MWT(timeout=10)
def positions():
    # Method to create a user's position table
    # Returns a df with the following information
    # Ticker, name, quantity, small_pos
    # THIS SHOULD CONTAIN THE STATIC FIELDS ONLY - no web requests
    # It should be a light method to load quickly on the main page.
    # Anything with web requests should be done on a separate function

    # Get all transactions & group by ticker name and operation
    df = transactions_fx()
    if df.empty:
        return df

    summary_table = df.groupby(['trade_asset_ticker', 'trade_operation'])[[
        "trade_quantity", "cash_value_fx", "trade_fees_fx"
    ]].sum()
    # Now let's create our main dataframe with information for each ticker
    list_of_tickers = df['trade_asset_ticker'].unique().tolist()
    main_df = pd.DataFrame({'trade_asset_ticker': list_of_tickers})
    # Fill with positions, cash_values and fees
    df_tmp = df.groupby(['trade_asset_ticker'])[[
        "trade_quantity", "cash_value_fx", "trade_fees_fx"
    ]].sum()
    main_df = pd.merge(main_df, df_tmp, on='trade_asset_ticker')
    # Fill in with same information but only for buys, sells, deposits and withdraws
    # main_df = pd.merge(main_df, summary_table, on='trade_asset_ticker')
    summary_table = summary_table.unstack(level='trade_operation').fillna(0)
    main_df = pd.merge(main_df, summary_table, on='trade_asset_ticker')
    # Include FIFO and LIFO calculations for each ticker
    main_df['cost_frame'] = main_df['trade_asset_ticker'].apply(
        cost_calculation)
    # Unpack this into multiple columns now
    main_df = df_unpack(main_df, 'cost_frame', 0)
    main_df = df_unpack(main_df, 'FIFO', 0)
    main_df = df_unpack(main_df, 'LIFO', 0)
    main_df['is_currency'] = main_df['trade_asset_ticker'].apply(is_currency)
    return main_df


def single_price(ticker):
    return (price_data_rt(ticker), datetime.now())


@ MWT(timeout=200)
def list_tickers():
    df = transactions_fx()
    # Now let's create our main dataframe with information for each ticker
    list_of_tickers = df['trade_asset_ticker'].unique().tolist()
    return (list_of_tickers)


@ MWT(timeout=2)
def positions_dynamic():
    # This method is the realtime updater for the front page. It gets the
    # position information from positions above and returns a dataframe
    # with all the realtime pricing and positions data - this method
    # should be called from an AJAX request at the front page in order
    # to reduce loading time.
    df = positions()
    # Drop all currencies from table
    df = df[df['is_currency'] == False]
    # check if trade_asset_ticker is set as index. If so, move to column
    # This happens on some memoized functions - need to understand why
    # The below is a temporary fix
    df = df.reset_index()
    if df is None:
        return None, None
    tickers_string = ",".join(list_tickers())
    # Let's try to get as many prices as possible into the df with a
    # single request - first get all the prices in current currency and USD
    multi_price = multiple_price_grab(tickers_string,
                                      'USD,' + fx_rate()['base'])

    # PARSER Function to find the ticker price inside the matrix. First part
    # looks into the cryptocompare matrix. In the exception, if price is not
    # found, it sends a request to other providers

    def find_data(ticker):
        notes = None
        try:
            # Parse the cryptocompare data
            FX = current_app.settings['PORTFOLIO']['base_fx']
            price = multi_price["RAW"][ticker][FX]["PRICE"]
            # GBTC should not be requested from multi_price as there is a
            # coin with same ticker
            if ticker == 'GBTC':
                raise
            price = float(price)
            high = float(multi_price["RAW"][ticker][FX]["HIGHDAY"])
            low = float(multi_price["RAW"][ticker][FX]["LOWDAY"])
            chg = multi_price["RAW"][ticker][FX]["CHANGEPCT24HOUR"]
            mktcap = multi_price["DISPLAY"][ticker][FX]["MKTCAP"]
            volume = multi_price["DISPLAY"][ticker][FX]["VOLUME24HOURTO"]
            last_up_source = multi_price["RAW"][ticker][FX]["LASTUPDATE"]
            source = multi_price["DISPLAY"][ticker][FX]["LASTMARKET"]
            last_update = datetime.now()
        except (KeyError, TypeError):
            # Couldn't find price with CryptoCompare. Let's try a different source
            # and populate data in the same format [aa = alphavantage]
            try:
                single_price = price_data_rt_full(ticker, 'aa')
                if single_price is None:
                    raise KeyError
                price = single_price[0]
                high = single_price[2]
                low = single_price[3]
                (_, last_update, _, _, chg, mktcap, last_up_source, volume,
                 source, notes) = single_price
            except Exception:
                # Let's try a final time using Financial Modeling Prep API
                try:
                    single_price = price_data_rt_full(ticker, 'fp')
                    if single_price is None:
                        raise KeyError
                    price = single_price[0]
                    high = single_price[2]
                    low = single_price[3]
                    (_, last_update, _, _, chg, mktcap, last_up_source, volume,
                     source, notes) = single_price
                except Exception:
                    try:
                        # Finally, if realtime price is unavailable, find the latest
                        # saved value in historical prices
                        # Create a price class
                        price_class = price_data(ticker)
                        if price_class is None:
                            raise KeyError
                        price = float(
                            price_class.df['close'].iloc[0]) * FX_RATE
                        high = float(price_class.df['high'].iloc[0]) * FX_RATE
                        low = float(price_class.df['low'].iloc[0]) * FX_RATE
                        volume = FX + "  " + "{0:,.0f}".format(
                            float(price_class.df['volume'].iloc[0]) * FX_RATE)
                        mktcap = chg = 0
                        source = last_up_source = 'Historical Data'
                        last_update = price_class.df.index[0]
                    except Exception:
                        price = high = low = chg = mktcap = last_up_source = last_update = volume = 0
                        source = '-'
        return price, last_update, high, low, chg, mktcap, last_up_source, volume, source, notes

    df = apply_and_concat(df, 'trade_asset_ticker', find_data, [
        'price', 'last_update', '24h_high', '24h_low', '24h_change', 'mktcap',
        'last_up_source', 'volume', 'source', 'notes'
    ])
    # Now create additional columns with calculations
    df['position_fx'] = df['price'] * df['trade_quantity']
    df['allocation'] = df['position_fx'] / df['position_fx'].sum()
    df['change_fx'] = df['position_fx'] * df['24h_change'] / 100
    # Pnl and Cost calculations
    df['breakeven'] = df['cash_value_fx'] / df['trade_quantity']
    df['pnl_gross'] = df['position_fx'] - df['cash_value_fx']
    df['pnl_net'] = df['pnl_gross'] - df['trade_fees_fx']
    # FIFO and LIFO PnL calculations
    df['LIFO_unreal'] = (df['price'] - df['LIFO_average_cost']) * \
        df['trade_quantity']
    df['FIFO_unreal'] = (df['price'] - df['FIFO_average_cost']) * \
        df['trade_quantity']
    df['LIFO_real'] = df['pnl_net'] - df['LIFO_unreal']
    df['FIFO_real'] = df['pnl_net'] - df['FIFO_unreal']
    df['LIFO_unrealized_be'] = df['price'] - \
        (df['LIFO_unreal'] / df['trade_quantity'])
    df['FIFO_unrealized_be'] = df['price'] - \
        (df['FIFO_unreal'] / df['trade_quantity'])
    # Allocations below 0.01% are marked as small
    # this is used to hide small and closed positions at html
    df.loc[df.allocation <= 0.0001, 'small_pos'] = 'True'
    df.loc[df.allocation >= 0.0001, 'small_pos'] = 'False'

    # Prepare for delivery. Change index, add total
    df.set_index('trade_asset_ticker', inplace=True)
    df.loc['Total'] = 0
    # Column names can't be tuples - otherwise json generates an error
    df.rename(columns={
        ('trade_quantity', 'B'): 'trade_quantity_B',
        ('trade_quantity', 'S'): 'trade_quantity_S',
        ('trade_quantity', 'D'): 'trade_quantity_D',
        ('trade_quantity', 'W'): 'trade_quantity_W',
        ('cash_value_fx', 'B'): 'cash_value_fx_B',
        ('cash_value_fx', 'S'): 'cash_value_fx_S',
        ('cash_value_fx', 'D'): 'cash_value_fx_D',
        ('cash_value_fx', 'W'): 'cash_value_fx_W',
        ('trade_fees_fx', 'B'): 'trade_fees_fx_B',
        ('trade_fees_fx', 'S'): 'trade_fees_fx_S',
        ('trade_fees_fx', 'D'): 'trade_fees_fx_D',
        ('trade_fees_fx', 'W'): 'trade_fees_fx_W'
    },
        inplace=True)

    # Need to add only some fields - strings can't be added for example
    columns_sum = [
        'cash_value_fx', 'trade_fees_fx', 'position_fx', 'allocation',
        'change_fx', 'pnl_gross', 'pnl_net', 'LIFO_unreal', 'FIFO_unreal',
        'LIFO_real', 'FIFO_real'
    ]
    for field in columns_sum:
        df.loc['Total', field] = df[field].sum()
    # Set the portfolio last update to be equal to the latest update in df
    df.loc['Total', 'last_up_source'] = (
        datetime.now()).strftime('%d-%b-%Y %H:%M:%S')
    df['last_update'] = df['last_update'].astype(str)
    # Create a pie chart data in HighCharts format excluding small pos
    pie_data = []
    for ticker in list_tickers():
        if df.loc[ticker, 'small_pos'] == 'False':
            tmp_dict = {}
            tmp_dict['y'] = round(df.loc[ticker, 'allocation'] * 100, 2)
            tmp_dict['name'] = ticker
            pie_data.append(tmp_dict)
    return (df, pie_data)


@ MWT(timeout=10)
def generatenav(user='mynode', force=False, filter=None):
    PORTFOLIO_MIN_SIZE_NAV = 1
    RENEW_NAV = 10
    FX = current_app.settings['PORTFOLIO']['base_fx']
    # Portfolios smaller than this size do not account for NAV calculations
    # Otherwise, there's an impact of dust left in the portfolio (in USD)
    # This is set in config.ini file
    min_size_for_calc = int(PORTFOLIO_MIN_SIZE_NAV)
    save_nav = True
    # This process can take some time and it's intensive to run NAV
    # generation every time the NAV is needed. A compromise is to save
    # the last NAV generation locally and only refresh after a period of time.
    # This period of time is setup in config.ini as RENEW_NAV (in minutes).
    # If last file is newer than 60 minutes (default), the local saved file
    # will be used.
    # Unless force is true, then a rebuild is done regardless
    # Local files are  saved under a hash of username.
    filename = "thewarden/nav_data/" + user + FX + ".nav"
    filename = os.path.join(current_path(), filename)
    if force:
        # Since this function can be run as a thread, it's safer to delete
        # the current NAV file if it exists. This avoids other tasks reading
        # the local file which is outdated
        try:
            os.remove(filename)
        except Exception:
            pass

    if not force:
        try:
            # Check if NAV saved file is recent enough to be used
            # Local file has to have a saved time less than RENEW_NAV min old
            modified = datetime.utcfromtimestamp(os.path.getmtime(filename))
            elapsed_seconds = (datetime.utcnow() - modified).total_seconds()

            if (elapsed_seconds / 60) < int(RENEW_NAV):
                nav_pickle = pd.read_pickle(filename)
                return (nav_pickle)
            else:
                pass

        except Exception:
            pass

    # Pandas dataframe with transactions
    df = transactions_fx()
    # if a filter argument was passed, execute it
    if filter:
        df = df.query(filter)
    start_date = df.index.min() - timedelta(
        days=1)  # start on t-1 of first trade
    end_date = datetime.today()

    # Create a list of all tickers that were traded in this portfolio
    tickers = list_tickers()

    # Create an empty DF, fill with dates and fill with operation and prices then NAV
    dailynav = pd.DataFrame(columns=['date'])
    # Fill the dates from first trade until today
    dailynav['date'] = pd.date_range(start=start_date, end=end_date)
    dailynav = dailynav.set_index('date')
    # Create empty fields
    dailynav['PORT_usd_pos'] = 0
    dailynav['PORT_fx_pos'] = 0
    dailynav['PORT_cash_value'] = 0
    dailynav['PORT_cash_value_fx'] = 0

    # Create a dataframe for each position's prices
    for id in tickers:
        if is_currency(id):
            continue
        try:
            # Create a new PriceData class for this ticker
            prices = price_data_fx(id)
            if prices is None:
                save_nav = False
                raise ValueError

            prices = prices.rename(columns={'close_converted': id + '_price'})
            prices = prices[id + '_price']
            # Fill dailyNAV with prices for each ticker

            # First check if prices is a Series. If so, convert to dataframe
            if isinstance(prices, pd.Series):
                prices = prices.to_frame()

            dailynav = pd.merge(dailynav, prices, on='date', how='left')

            # Replace NaN with prev value, if no prev value then zero
            dailynav[id + '_price'].fillna(method='ffill', inplace=True)
            dailynav[id + '_price'].fillna(0, inplace=True)

            # Now let's find trades for this ticker and include in dailynav
            tradedf = df[[
                'trade_asset_ticker', 'trade_quantity', 'cash_value_fx'
            ]]
            # Filter trades only for this ticker
            tradedf = tradedf[tradedf['trade_asset_ticker'] == id]
            # consolidate all trades in a single date Input
            tradedf = tradedf.groupby(level=0).sum()
            tradedf.sort_index(ascending=True, inplace=True)
            # include column to cumsum quant
            tradedf['cum_quant'] = tradedf['trade_quantity'].cumsum()
            # merge with dailynav - 1st rename columns to match
            tradedf.index.rename('date', inplace=True)
            # rename columns to include ticker name so it's differentiated
            # when merged with other ids
            tradedf.rename(columns={
                'trade_quantity': id + '_quant',
                'cum_quant': id + '_pos',
                'cash_value_fx': id + '_cash_value_fx'
            },
                inplace=True)
            # merge
            dailynav = pd.merge(dailynav, tradedf, on='date', how='left')
            # for empty days just trade quantity = 0, same for CV
            dailynav[id + '_quant'].fillna(0, inplace=True)
            dailynav[id + '_cash_value_fx'].fillna(0, inplace=True)
            # Now, for positions, fill with previous values, NOT zero,
            # unless there's no previous
            dailynav[id + '_pos'].fillna(method='ffill', inplace=True)
            dailynav[id + '_pos'].fillna(0, inplace=True)
            # Calculate USD and fx position and % of portfolio at date
            # Calculate USD position and % of portfolio at date
            dailynav[id + '_fx_pos'] = dailynav[id + '_price'].astype(
                float) * dailynav[id + '_pos'].astype(float)
            # Before calculating NAV, clean the df for small
            # dust positions. Otherwise, a portfolio close to zero but with
            # 10 sats for example, would still have NAV changes
            dailynav[id + '_fx_pos'].round(2)

        except Exception as e:
            flash(f"An error has ocurred {str(e)}", "danger")
    # Another loop to sum the portfolio values - maybe there is a way to
    # include this on the loop above. But this is not a huge time drag unless
    # there are too many tickers in a portfolio
    for id in tickers:
        if is_currency(id):
            continue
        # Include totals in new columns
        try:
            dailynav['PORT_fx_pos'] = dailynav['PORT_fx_pos'] +\
                dailynav[id + '_fx_pos']
        except KeyError as e:
            save_nav = False
            flash(
                "Ticker " + id + " was not found on NAV table. " +
                "NAV calculations will be off. Error: " + str(e), "danger")
            continue
        dailynav['PORT_cash_value_fx'] = dailynav['PORT_cash_value_fx'] +\
            dailynav[id + '_cash_value_fx']

    # Now that we have the full portfolio value each day, calculate alloc %
    for id in tickers:
        if is_currency(id):
            continue
        try:
            dailynav[id + "_fx_perc"] = dailynav[id + '_fx_pos'] /\
                dailynav['PORT_fx_pos']
            dailynav[id + "_fx_perc"].fillna(0, inplace=True)
        except KeyError:
            continue

    # Create a new column with the portfolio change only due to market move
    # discounting all cash flows for that day
    dailynav['adj_portfolio_fx'] = dailynav['PORT_fx_pos'] -\
        dailynav['PORT_cash_value_fx']

    # For the period return let's use the Modified Dietz Rate of return method
    # more info here: https://tinyurl.com/y474gy36
    # There is one caveat here. If end value is zero (i.e. portfolio fully
    # redeemed, the formula needs to be adjusted)
    dailynav.loc[dailynav.PORT_fx_pos > min_size_for_calc,
                 'port_dietz_ret_fx'] = ((dailynav['PORT_fx_pos'] -
                                          dailynav['PORT_fx_pos'].shift(1)) -
                                         dailynav['PORT_cash_value_fx']) /\
        (dailynav['PORT_fx_pos'].shift(1) +
         abs(dailynav['PORT_cash_value_fx']))

    # Fill empty and NaN with zero
    dailynav['port_dietz_ret_fx'].fillna(0, inplace=True)
    dailynav['adj_port_chg_fx'] = (
        (dailynav['PORT_fx_pos'] - dailynav['PORT_fx_pos'].shift(1)) -
        dailynav['PORT_cash_value_fx'])

    # let's fill NaN with zeros
    dailynav['adj_port_chg_fx'].fillna(0, inplace=True)
    # Calculate the metrics
    dailynav['port_perc_factor_fx'] = (dailynav['port_dietz_ret_fx']) + 1
    dailynav['NAV_fx'] = dailynav['port_perc_factor_fx'].cumprod()
    dailynav['NAV_fx'] = dailynav['NAV_fx'] * 100
    dailynav['PORT_ac_CFs_fx'] = dailynav['PORT_cash_value_fx'].cumsum()

    # Save NAV Locally as Pickle
    if save_nav:
        filename = "thewarden/nav_data/" + user + FX + ".nav"
        filename = os.path.join(current_path(), filename)
        # makesure file path exists
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != 17:
                raise
        dailynav.to_pickle(filename)

    return dailynav


def clear_memory():
    for name in dir():
        if not name.startswith('_'):
            del globals()[name]

    for name in dir():
        if not name.startswith('_'):
            del locals()[name]


def regenerate_nav():
    # re-generates the NAV on the background - delete First
    # the local NAV file so it's not used.
    # Check if there any trades in the database. If not, skip.
    try:
        # Delete all pricing history
        filename = os.path.join(current_path(),
                                'thewarden/pricing_engine/pricing_data/*.*')
        aa_files = glob.glob(filename)
        [os.remove(x) for x in aa_files]
        filename = os.path.join(current_path(), 'thewarden/nav_data/*.*')
        nav_files = glob.glob(filename)
        [os.remove(x) for x in nav_files]
        # Clear memory, cache
        clear_memory()
        MWT()._caches = {}
        MWT()._timeouts = {}
        generatenav('mynode', force=True)
    except Exception:
        return


@ MWT(timeout=60)
def cost_calculation(ticker, html_table=None):
    # This function calculates the cost basis assuming 3 different methods
    # FIFO, LIFO and avg. cost
    # If html_table is set to either FIFO or LIFO, it will return
    # an html table for this ticker

    # Gets all transactions in local currency terms
    df = transactions_fx()
    df = df[(df.trade_asset_ticker == ticker)]

    # Find current open position on asset
    summary_table = df.groupby(['trade_asset_ticker', 'trade_operation'])[[
        "cash_value", "cash_value_fx", "trade_fees", "trade_quantity"
    ]].sum()

    open_position = summary_table.sum()['trade_quantity']

    # Drop Deposits and Withdraws - keep only Buy and Sells
    if open_position > 0:
        df = df[df.trade_operation.str.match('B')]
    elif open_position < 0:
        df = df[df.trade_operation.str.match('S')]

    # Let's return a dictionary for this user with FIFO, LIFO and Avg. Cost
    cost_matrix = {}

    # ---------------------------------------------------
    # FIFO
    # ---------------------------------------------------
    fifo_df = df.sort_index(ascending=False)
    fifo_df['acum_Q'] = fifo_df['trade_quantity'].cumsum()
    fifo_df['acum_Q'] = np.where(fifo_df['acum_Q'] < open_position,
                                 fifo_df['acum_Q'], open_position)
    # Keep only the number of rows needed for open position
    fifo_df = fifo_df.drop_duplicates(subset="acum_Q", keep='first')
    fifo_df['Q'] = fifo_df['acum_Q'].diff()
    fifo_df['Q'] = fifo_df['Q'].fillna(fifo_df['acum_Q'])
    # if fifo_df['acum_Q'].count() == 1:
    #     fifo_df['Q'] = fifo_df['acum_Q']
    # Adjust Cash Value only to account for needed position
    fifo_df['adjusted_cv'] = fifo_df['cash_value_fx'] * fifo_df['Q'] /\
        fifo_df['trade_quantity']
    cost_matrix['FIFO'] = {}
    cost_matrix['FIFO']['FIFO_cash'] = fifo_df['adjusted_cv'].sum()
    cost_matrix['FIFO']['FIFO_quantity'] = open_position
    cost_matrix['FIFO']['FIFO_count'] = int(fifo_df['trade_operation'].count())
    cost_matrix['FIFO']['FIFO_average_cost'] = fifo_df['adjusted_cv'].sum()\
        / open_position

    # ---------------------------------------------------
    #  LIFO
    # ---------------------------------------------------
    lifo_df = df.sort_index(ascending=True)
    lifo_df['acum_Q'] = lifo_df['trade_quantity'].cumsum()
    lifo_df['acum_Q'] = np.where(lifo_df['acum_Q'] < open_position,
                                 lifo_df['acum_Q'], open_position)
    # Keep only the number of rows needed for open position
    lifo_df = lifo_df.drop_duplicates(subset="acum_Q", keep='first')
    lifo_df['Q'] = lifo_df['acum_Q'].diff()
    lifo_df['Q'] = lifo_df['Q'].fillna(lifo_df['acum_Q'])
    # if lifo_df['acum_Q'].count() == 1:
    #     lifo_df['Q'] = lifo_df['acum_Q']
    # Adjust Cash Value only to account for needed position
    lifo_df['adjusted_cv'] = lifo_df['cash_value_fx'] * lifo_df['Q'] /\
        lifo_df['trade_quantity']

    cost_matrix['LIFO'] = {}
    cost_matrix['LIFO']['LIFO_cash'] = lifo_df['adjusted_cv'].sum()
    cost_matrix['LIFO']['LIFO_quantity'] = open_position
    cost_matrix['LIFO']['LIFO_count'] = int(lifo_df['trade_operation'].count())
    cost_matrix['LIFO']['LIFO_average_cost'] = lifo_df['adjusted_cv'].sum(
    ) / open_position

    if html_table == "FIFO":
        # Format the df into an HTML table to be served at main page
        html = fifo_df[[
            'trade_operation', 'Q', 'acum_Q', 'trade_price_fx',
            'trade_fees_fx', 'cash_value_fx', 'adjusted_cv',
            'trade_reference_id'
        ]]

    if html_table == "LIFO":
        html = lifo_df[[
            'trade_operation', 'Q', 'acum_Q', 'trade_price_fx',
            'trade_fees_fx', 'cash_value_fx', 'adjusted_cv',
            'trade_reference_id'
        ]]

    # Now format the HTML properly
    if html_table:
        fx = FX
        # Include a link to edit this transaction
        html["trade_reference_id"] = "<a href='/edittransaction?reference_id=" +\
            html['trade_reference_id'] +\
            "'><i class='fas fa-edit'></i></a>"

        html.index = pd.to_datetime(html.index).strftime('%Y-%m-%d')
        # Include TOTAL row
        html.loc['TOTAL'] = 0
        # Need to add only some fields - strings can't be added for example
        columns_sum = ['Q', 'trade_fees_fx', 'cash_value_fx', 'adjusted_cv']
        for field in columns_sum:
            html.loc['TOTAL', field] = html[field].sum()

        # format numbers
        html['acum_Q'] = abs(html['acum_Q'])
        html['Q'] = abs(html['Q'])
        html['acum_Q'] = html['acum_Q'].map('{:,.4f}'.format)
        html['Q'] = html['Q'].map('{:,.4f}'.format)
        html['trade_price_fx'] = html['trade_price_fx'].map('{:,.2f}'.format)
        html['trade_fees_fx'] = html['trade_fees_fx'].map('{:,.2f}'.format)
        html['cash_value_fx'] = html['cash_value_fx'].map('{:,.2f}'.format)
        html['adjusted_cv'] = html['adjusted_cv'].map('{:,.2f}'.format)
        html.loc['TOTAL', 'trade_operation'] = ''
        html.loc['TOTAL', 'acum_Q'] = ''
        html.loc['TOTAL', 'trade_price_fx'] = ''
        html.loc['TOTAL', 'trade_reference_id'] = ''
        html = html.rename(
            columns={
                'trade_operation': 'B/S',
                'acum_Q': 'Q (acum)',
                'trade_price_fx': 'Price (' + fx + ')',
                'trade_fees_fx': 'Fees (' + fx + ')',
                'cash_value_fx': 'Cash Flow (' + fx + ')',
                'adjusted_cv': 'Adj CF (' + fx + ')',
                'trade_reference_id': ' '
            })

        cost_matrix = html.to_html(
            classes='table table-condensed table-striped small-text text-right',
            escape=False,
            index_names=False,
            justify='right')

    return (cost_matrix)


def fx_list():
    filename = os.path.join(current_path(),
                            'static/csv_files/physical_currency_list.csv')
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        fiat_dict = {rows[0]: (rows[1]) for rows in reader}
    # Convert dict to list
    fx_list = [(k, k + ' | ' + v) for k, v in fiat_dict.items()]
    fx_list.sort()
    return (fx_list)


def is_currency(id):
    # Return true if id is in list of currencies
    found = ([item for item in fx_list() if item[0] == id])
    if found != []:
        return True
    return False


def to_epoch(in_date):
    return str(int((in_date - datetime(1970, 1, 1)).total_seconds()))


# Keep only n last lines of file
def tail(f, lines=20):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0, 0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

# ---------------- PANDAS HELPER FUNCTION --------------------------
# This is a function to concatenate a function returning multiple columns into
# a dataframe.


def apply_and_concat(dataframe, field, func, column_names):
    return pd.concat((dataframe, dataframe[field].apply(
        lambda cell: pd.Series(func(cell), index=column_names))),
        axis=1)


# ---------------- PANDAS HELPER FUNCTION --------------------------
# Pandas helper function to unpack a dictionary stored within a
# single pandas column cells.
def df_unpack(df, column, fillna=None):
    ret = None
    if fillna is None:
        ret = pd.concat(
            [df, pd.DataFrame((d for idx, d in df[column].iteritems()))],
            axis=1)
        del ret[column]
    else:
        ret = pd.concat([
            df,
            pd.DataFrame(
                (d for idx, d in df[column].iteritems())).fillna(fillna)
        ],
            axis=1)
        del ret[column]
    return ret
