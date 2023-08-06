import getpass
import paramiko as pm
import re

from os import path as p
from os import  listdir

def get_files(username:str=None, password:str=None, save_path:str=None):
    """
    :param username: Your Clever SFTP username
    
    :param password: Your Clever SFTP password
    
    :param filepath: The location you wish to save your files.  If a path is 
    provided then the script will default to using its own internal folder 
    structure
        Data/
            DailyParticipation/
                Staff/
                Students/
                Teachers/
            ResourceUsage/
                Staff/
                Students/
                Teachers/

    :return: a list of file paths containing only files that were added in the
    most recent run of the script.
    """
    host = "reports-sftp.clever.com"
    port = 22
    transport = pm.Transport((host, port))

    transport.connect(username=username, password=password)

    sftp = pm.SFTPClient.from_transport(transport)

    search_pattern = (
        f"(participation-staff)|(participation-teachers)|"
        f"(participation-students)|(resource-usage-staff)|"
        f"(resource-usage-students)|(resource-usage-teachers)"
    )

    file_joins = {
        "participation-staff": ("Data", "DailyParticipation", "Staff"),
        "participation-teachers": ("Data", "DailyParticipation", "Teachers"),
        "participation-students": ("Data", "DailyParticipation", "Students"),
        "resource-usage-staff": ("Data", "ResourceUsage", "Staff"),
        "resource-usage-teachers": ("Data", "ResourceUsage", "Teachers"),
        "resource-usage-students": ("Data", "ResourceUsage", "Students")
    }
    new_files = []
    for folder in sftp.listdir():
        sftp.chdir(folder)
        for file in sftp.listdir():
            if save_path:
                path = save_path
            else:
                path_joins = file_joins[re.search(search_pattern, file)[0]]
                path = p.join(
                    p.dirname(p.abspath(__file__)),
                    path_joins[0],
                    path_joins[1],
                    path_joins[2]
                )
            file_list = listdir(path)
            if file in file_list:
                pass
            else:
                save_file = p.join(path, file)
                sftp.get(file, save_file)
                new_files.append(save_file)
        sftp.chdir("..")

    return new_files
