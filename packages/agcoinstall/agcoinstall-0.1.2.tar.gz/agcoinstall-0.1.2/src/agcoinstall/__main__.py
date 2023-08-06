"""Command-line interface."""
import base64
import fileinput
import hashlib
import hmac
import logging
import os
import random
import site
# from win32com.client import Dispatch
import subprocess
import time
import json
import configparser
import xml.etree.ElementTree as ET
from collections import defaultdict

import arrow
import click
import psutil
import regobj
import requests
import pyautogui
from requests.auth import AuthBase

host = ''
base_url = ''
mac_id = ''
mac_token = ''
state = 'InitialMonitoring'

logging.basicConfig(filename='agcoinstall.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


class MACAuth(AuthBase):
    """
    Attaches HTTP Authentication to the given Request object, and formats the header for every API call used
    """

    def __init__(self, mac_id, mac_token, host):
        # setup any auth-related data here
        self.mac_id = mac_id
        self.mac_token = mac_token
        self.host = host

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.generate_header(r.method, r.path_url)
        return r

    def get_hmac(self, method, uri, milliseconds, nonce):
        http_version = 'HTTP/1.1'
        # host = HOST
        request_string = f'{method} {uri} {http_version}\n{self.host}\n{milliseconds}\n{nonce}\n'
        return base64.b64encode(
            hmac.new(self.mac_token.lower().encode(), request_string.encode(), hashlib.sha256).digest()).decode()

    def generate_header(self, method, uri):
        milliseconds = str(int(time.time() * 1000))
        nonce = ''.join([str(random.randint(0, 9)) for i in range(8)])
        formatted_hmac = self.get_hmac(method, uri, milliseconds, nonce)
        return f'MAC kid={self.mac_id},ts={milliseconds},nonce={nonce},mac=\"{formatted_hmac}\"'


def download_auc_client():
    url = 'https://agcoedtdyn.azurewebsites.net/AGCOUpdateClient'
    save_path = os.path.expanduser('~\\Desktop\\AGCOUpdateClient.exe')
    try:
        r = requests.get(url, allow_redirects=True)
        try:
            open(save_path, 'wb').write(r.content)
        except:
            logging.error('Unable to download the AUC client')
    except:
        logging.error('The link to download the latest AUC is down')


def install_auc():
    execute_command(os.path.expanduser('~\\Desktop\\AGCOUpdateClient.exe /S /V INITCLIENT 1'))


def active_packages():
    parser = configparser.ConfigParser()
    try:
        parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
        active_packages_string = parser.get('Status', 'ActivePackages')
        logging.info(f'Number of active packages in AUC: {active_packages_string}')
    except:
        active_packages_string = 0
    return int(active_packages_string)


def pause_downloads_set():
    parser = configparser.ConfigParser()
    try:
        parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
        download_schedule_value = parser.get('Settings', 'DownloadSchedule')
        logging.info(f'DownloadSchedule: {download_schedule_value}')
        result = 'toggle' in download_schedule_value
    except:
        click.secho('Could not read config.ini for Settings>>DownloadScheldue')
        result = False
    return result


def ready_to_install():
    if os.path.isfile(r"C:\ProgramData\AGCO Corporation\AGCO Update\config.ini"):
        try:
            parser = configparser.ConfigParser()
            parser.read(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')
            ready_to_install_value = parser.get('Status', 'ReadyToInstall')
            logging.debug(f'ReadyToInstallValue: {ready_to_install_value}')
            return ready_to_install_value
        except configparser.NoSectionError as e:
            print(e)
            logging.exception(e)
            time.sleep(5)
        except AttributeError as e:
            print(e)
            logging.exception(e)
            time.sleep(5)
        return ""
    else:
        return ""


def config_ini_find_and_replace(find_text, replace_text):
    logging.info(f'Attempting to replace \"{find_text}\" with \"{replace_text}\" in the config.ini file')
    kill_process_by_name('AGCOUpdateService')
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace(find_text, replace_text), end='')
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def set_auc_environment(env_base_url):
    # other_urls = set(remaining_urls.values())
    logging.info(f'Attempting to set the env url of {env_base_url} in the config.ini file')
    kill_process_by_name('AGCOUpdateService')
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\test.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            if "UpdateHost" in line:
                line = f'UpdateHost=https://{env_base_url}/api/v2\n'
            print(line, end='')
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def restart_auc():
    logging.info(f'Attempting to restart AUC')
    kill_process_by_name('AGCOUpdateService')
    set_service_running('AGCO Update')
    start_auc()
    time.sleep(10)


def launch_edt():
    logging.debug('Attempting to start EDT')
    execute_command(r'"C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe" EDT')


def set_config_ini_to_original():
    with fileinput.FileInput(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini', inplace=True,
                             backup='.bak') as file:
        for line in file:
            print(line.replace('IsExplicitInstallRunning=True', 'IsExplicitInstallRunning=False'), end='')


def execute_command(path_and_command):
    """
    Runs an inputted command. If the command returns a non-zero return code it will fail. This method is not for
    capturing the output
    """
    logging.debug(f'Attempting to execute: {path_and_command}')
    p1 = subprocess.run(path_and_command,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True,
                        )
    logging.debug(f'Command: {path_and_command}')
    logging.debug(f'ReturnCode: {str(p1.returncode)}')


def kill_process_by_name(process_name):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        current_proc_name = proc.info['name']
        if process_name in current_proc_name:
            logging.info(f'Killing process: {current_proc_name}')
            try:
                proc.kill()
                logging.debug(f'Killed process: {current_proc_name}')
            except:
                logging.debug(f'Unable to kill process: {current_proc_name}')


def start_auc():
    logging.debug('Attempting to start AUC')
    try:
        os.startfile(r'C:\Program Files (x86)\AGCO Corporation\AGCO Update Client\AGCOUpdateService.exe')
    except:
        logging.error('Unable to start AGCOUpdateService.exe')


def apply_certs():
    logging.info('Attempting to apply Trusted Publish certificates')
    for loc in site.getsitepackages():
        if "site-packages" in loc:
            site_loc = loc
        else:
            logging.error('Site-packages were not found for this Python version')
    subprocess.call(
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe certutil -addstore TrustedPublisher "
        fr"{site_loc}\agcoinstall\data\SontheimCertificate1.cer", shell=True)
    subprocess.call(
        r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe certutil -addstore TrustedPublisher "
        fr"{site_loc}\agcoinstall\data\SontheimCertificate2.cer", shell=True)


def set_service_running(service):
    """
    Sets a windows service's start-up type to running
    :param service: string name of windows service
    """
    logging.debug(f'Attempting to set the following service to running: {service}')

    p1 = subprocess.run(fr'net start "{service}"',
                        shell=True,
                        capture_output=True,
                        text=True,
                        check=True,
                        )
    save_path = os.path.expanduser('~\\Desktop\\')
    with open(fr'{save_path}temp_output.txt', 'w') as f:
        f.write(p1.stdout)
    with open(fr'{save_path}temp_output.txt', 'r') as f:
        for line in f.readlines():
            if f"The {service} service was started successfully." in line:
                logging.debug(f"{service} has started")


def set_edt_environment(env_base_url):
    files = [r'C:\Program Files (x86)\AGCO Corporation\EDT\EDTUpdateService.exe.config',
             r'C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe.config']
    for file in files:
        mytree = ET.parse(file)
        myroot = mytree.getroot()
        for child in myroot.iter('value'):
            if 'https' in child.text:
                child.text = fr'https://{env_base_url}/api/v2'
        mytree.write(file)


def apply_voucher():
    voucher = create_voucher()
    logging.info(f'Applying voucher via command line \"AgcoGT.exe APPLYVoucher {voucher} NA0001 30096\"')
    execute_command(rf'"C:\Program Files (x86)\AGCO Corporation\EDT\AgcoGT.exe" APPLYVoucher {voucher} NA0001 30096')


def get_client_id():
    try:
        return (
            regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation')
                .get_subkey(r'AGCO Update')['ClientID']
                .data
        )
    except AttributeError as e:
        click.secho("Client Id was not present in registry. Please confirm that you have AUC installed \n{e}", fg='red')


def edt_is_vouchered():
    """
    gets and return the voucher in the registry
    @return: voucher code as text
    """
    try:
        voucher_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['Voucher'].data
    except AttributeError as e:
        click.secho(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}', fg='red')
        logging.error(f'Voucher ID was not present in registry. Please confirm that EDT has been vouchered {e}')
        voucher_id = ''
    except KeyError:
        voucher_id = ''
    return voucher_id


def edt_is_installed():
    """
        gets and return the voucher in the registry
        @return: voucher code as text
        """
    try:
        edt_update = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['UpdateNumber'].data
    except AttributeError as e:
        click.secho(f'UpdateNumber was not present in registry. It does not appear that EDT is currently installed.',
                    fg='red')
        edt_update = ''
    except KeyError:
        edt_update = ''
    return edt_update


def core_installed():
    """
        gets and return the voucher in the registry
        @return: voucher code as text
    """
    try:
        mtapi = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').EDT['MTAPISync_Version'].data
    except AttributeError as e:
        click.secho(f'UpdateNumber was not present in registry. It does not appear that EDT is currently installed.',
                    fg='red')
        mtapi = ''
    except KeyError:
        mtapi = ''
    return mtapi


def get_reg_client_id():
    try:
        client_id = regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
            'ClientID'].data
    except AttributeError as e:
        click.secho(
            f'Client ID was not present in registry. Please confirm that you have AGCO update client installed. {e}',
            fg='red')
        client_id = ''
    return client_id


def bypass_download_scheduler():
    """Bypasses the download Scheduler by writing a line in the registry that the current AUC checks before applying
    the download scheduler"""
    current_time = arrow.utcnow().format('MM/DD/YYYY h:mm:ss A')
    try:
        regobj.HKLM.SOFTWARE.WOW6432Node.get_subkey(r'AGCO Corporation').get_subkey(r'AGCO Update')[
            'AUCConfiguration.LastExecutedUTC'] = current_time
    except AttributeError as e:
        logging.error(
            f'AGCO Update was not found in the registry. Please confirm that you have AGCO update client '
            f'installed. {e}')
        click.secho(f'AGCO Update was not found in the registry. Please confirm that you have AGCO update client '
                    f'installed. {e}', fg='red')


def get_date_x_weeks_from_now(number_of_weeks=8):
    utc = arrow.utcnow()
    x_weeks_from_now = utc.shift(weeks=+number_of_weeks)
    return x_weeks_from_now.isoformat()


def create_voucher(duration=8):
    """Creates temporary voucher"""
    expire_date = get_date_x_weeks_from_now(duration)
    logging.info(f'Attempting to create a voucher that expires {expire_date}')
    uri = f'{base_url}/api/v2/Vouchers'
    payload = {
        "Type": "Temporary",
        "DealerCode": "NA0001",
        "LicenseTo": "Darrin Fraser",
        "Purpose": "Testing",
        "Email": "darrin.fraser@agcocorp.com",
        "ExpirationDate": expire_date,
    }
    r = requests.post(f'{uri}', auth=MACAuth(mac_id, mac_token, host), data=payload)
    return r.text.strip('"')


def get_client_relationships(client_id):
    uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
    payload = {
        "limit": 100,
        "ClientID": client_id
    }
    r = requests.get(uri, auth=MACAuth(mac_id, mac_token, host), params=payload)
    returned_relationships = json.loads(r.text)
    ug_client_relationship_list = returned_relationships['Entities']
    return ug_client_relationship_list


def subscribe_or_update_client_relationships(ug_to_be_assigned, ug_client_relationships, remove_ug_dict, client_id):
    ugs_to_be_removed = set(remove_ug_dict.values())
    to_be_assigned_in_relationships = False
    for relationship in ug_client_relationships:
        if ug_to_be_assigned == relationship['UpdateGroupID'] and relationship['Active'] is True:
            to_be_assigned_in_relationships = True

        if relationship['UpdateGroupID'] in ugs_to_be_removed and relationship['Active'] is True:
            relationship['Active'] = False
            relationship_id = relationship['RelationshipID']
            uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
            r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)

        if relationship['UpdateGroupID'] == ug_to_be_assigned and relationship['Active'] is False:
            relationship['Active'] = True
            relationship_id = relationship['RelationshipID']
            uri = f'{base_url}/api/v2/UpdateGroupClientRelationships/{relationship_id}'
            r = requests.put(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)
            to_be_assigned_in_relationships = True

    if not to_be_assigned_in_relationships:
        ug_plus_basic_inventory = [ug_to_be_assigned, 'f23c4a77-a200-4551-bf61-64aef94c185e']
        for ug in ug_plus_basic_inventory:
            try:
                uri = f'{base_url}/api/v2/UpdateGroupClientRelationships'
                relationship = {'UpdateGroupID': ug_to_be_assigned,
                                'ClientID': client_id,
                                'Active': True,
                                }
                r = requests.post(uri, auth=MACAuth(mac_id, mac_token, host), data=relationship)
            except Exception as ex:
                logging.error(f'There was an error assigning UpdateGroup: {ug}...\n{ex}')


def click_on_image(imagefile):
    logging.info(f'Attempting to click on {imagefile}')
    center = pyautogui.locateCenterOnScreen(imagefile)
    pyautogui.click(center)


def file_watcher():
    global state
    moddate = os.stat(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')[8]
    logging.debug(f'Starting file_watcher module: {moddate}')
    while True:
        current_moddate = os.stat(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini')[8]
        if current_moddate == moddate:
            time.sleep(5)
        else:
            logging.info("Change detected...testing for state")
            moddate = current_moddate
            current_state = get_state()
            if current_state != state:
                if current_state == 'DownloadsPaused':
                    state = 'DownloadsPaused'
                    config_ini_find_and_replace('DownloadSchedule=Start: On  Toggle: 06:00, 18:00',
                                                'DownloadSchedule=Start: On')

                if current_state == 'ReadyToInstallCorePackages':
                    state = 'ReadyToInstallCorePackages'
                    config_ini_find_and_replace('IsExplicitInstallRunning=False', 'IsExplicitInstallRunning=True')

                if current_state == 'ReadyToInstallAdditional':
                    state = 'ReadyToInstallAdditional'
                    config_ini_find_and_replace('IsExplicitInstallRunning=False', 'IsExplicitInstallRunning=True')

                if current_state == 'EDTNeedsVouchered':  ##TODO this will vary depending on environment
                    state = 'EDTNeedsVouchered'
                    apply_voucher()
                    launch_edt()

                if current_state == 'AllDownloadsCompleted':
                    state = 'AllDownloadsCompleted'
                    click.secho('All downloads are complete closing Watcher')
                    break


def models_are_installed():
    return os.path.isdir(r'C:\ProgramData\AGCO Corporation\EDT\Models')


def get_state():
    if os.path.isfile(r'C:\ProgramData\AGCO Corporation\AGCO Update\config.ini'):
        global state
        install_ready = ready_to_install()
        number_of_packages = active_packages()
        edt_vouchered = edt_is_vouchered()
        edt_installed = edt_is_installed()
        dl_paused = pause_downloads_set()
        models_installed = models_are_installed()
        core_is_installed = core_installed()
        current_state = ''
    else:
        time.sleep(5)

    if install_ready and not edt_installed:
        logging.info("Changing current_state to ReadyToInstallCorePackages")
        current_state = "ReadyToInstallCorePackages"

    elif install_ready and edt_installed and edt_vouchered and number_of_packages != 0:
        logging.info("Changing current_state to ReadyToInstallAdditional")
        current_state = "ReadyToInstallAdditional"

    elif not install_ready and edt_installed and number_of_packages == 0 and not edt_vouchered:
        logging.info("Changing current_state to EDTNeedsVouchered")
        current_state = 'EDTNeedsVouchered'

    elif dl_paused and number_of_packages > 1:
        logging.info("Changing current_state to DownloadsPaused")
        current_state = 'DownloadsPaused'

    elif number_of_packages == 0 and not install_ready and edt_installed and edt_vouchered:
        logging.info("Changing current_state to AllDownloadsCompleted")
        current_state = 'AllDownloadsCompleted'

    else:
        current_state = 'InitialMonitoring'

    return current_state


@click.command()
@click.version_option()
@click.option('--env', '-e', default='prod', type=click.Choice(['prod', 'test', 'dev']))
@click.option('--auc_env_change', '-aec', is_flag=True)
@click.option('--updategroup', '-ug', default='InternalTestPush', type=click.Choice(['EDTUpdates',
                                                                                     'Dev',
                                                                                     'RC',
                                                                                     'TestPush',
                                                                                     'InternalTestPush',
                                                                                     'InternalDev',
                                                                                     'InternalRC',
                                                                                     ]))
@click.option('--m_id', '-mi', prompt=True, default=lambda: os.environ.get('MAC_ID', ''), help="Supply MAC_ID")
@click.option('--m_token', '-mt', prompt=True, default=lambda: os.environ.get('MAC_TOKEN', ''), help="Supply MAC_TOKEN")
def main(env, auc_env_change, updategroup, m_id, m_token) -> None:
    """Agcoinstall."""

    global host, base_url, mac_id, mac_token
    mac_id = m_id
    mac_token = m_token

    ug_dict = {'EDTUpdates': 'eb91c5e8-ffb1-4060-8b97-cb53dcd4858d',
               'Dev': '29527dd4-3828-40f1-91b4-dfa83774e0c5',
               'RC': '30ae5793-67a2-4111-a94a-876a274c3814',
               'InternalTestPush': 'd76d7786-1771-4d3b-89b1-c938061da4ca',
               'TestPush': '42dd2226-cdaa-46b4-8e23-aa98ec790139',
               'InternalDev': '6ed348f3-8e77-4051-a570-4d2a6d86995d',
               'InternalRC': "75a00edd-417b-459f-80d9-789f0c341131",
               }

    env_dict = {'dev': 'edtsystems-webtest-dev.azurewebsites.net',
                'prod': 'secure.agco-ats.com',
                'test': 'edtsystems-webtest.azurewebsites.net',
                }

    update_group_id = ug_dict.pop(updategroup)

    host = env_dict[env]
    base_url = f'https://{host}'

    apply_certs()
    if not os.path.isdir(r'C:\ProgramData\AGCO Corporation\AGCO Update'):
        download_auc_client()
        install_auc()
    cid = get_client_id()
    bypass_download_scheduler()
    c_relationships = get_client_relationships(cid)
    subscribe_or_update_client_relationships(update_group_id, c_relationships, ug_dict, cid)
    if auc_env_change:
        set_auc_environment()
    restart_auc()
    time.sleep(10)
    file_watcher()
    set_edt_environment(host)


if __name__ == "__main__":
    main(prog_name="agcoinstall")  # pragma: no cover
