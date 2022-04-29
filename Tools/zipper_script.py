from zipfile import ZipFile
import os
import time
import shutil


def zip_files(files, entry, exit, zip_limit):
    zip_size = 0
    os.chdir(entry)

    zip_file = time.strftime('gway-' + '%Y%m%d_%H%M%S' + '.zip')

    with ZipFile(zip_file, mode='a') as archive:

        for file in files[:]:
            temp = zip_size + file['size']

            if temp <= zip_limit:
                archive.write(file['filename'])
                zip_size += file['size']
                files.remove(file)
                print('{:<30} {:<30} {:<20}'.format(
                    file['filename'], str(file['date']), str(zip_size)))
                # os.remove(file['filename']) # REMOVE WHEN DONE FOR COMPLETE FILE TRANSFER

    shutil.move(zip_file, exit)

    rem_data = [f['size'] for f in files if(f['size'] < zip_limit)]

    if len(rem_data) > 0:
        time.sleep(1)
        zip_files(files, entry, exit, zip_limit)
    else:
        print("\nZipping Complete!\n")


def zip_handler():
    # input validation
    while True:
        try:
            entry_dir = input('Please enter entry directory: ')
            if os.path.exists(entry_dir):
                break
            else:
                raise
        except:
            print("Entry directory doesn't exist!\n")

    while True:
        try:
            exit_dir = input('Please enter exit directory: ')
            if os.path.exists(exit_dir):
                break
            else:
                raise
        except:
            print("Exit directory doesn't exist!\n")

    while True:
        try:
            zip_limit = int(input('Please enter maximum zip size(Bytes): '))
            if zip_limit < 1000:
                raise
            else:
                break
        except:
            print("Invalid input!\n")

    # file processing/validation
    files = []
    for file in os.listdir(entry_dir):
        path = os.path.join(entry_dir, file)

        if os.path.isdir(path) or file.endswith('.zip'):
            continue

        file_size = os.path.getsize(path)
        file_date = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path)))
        files.append({'filename': file, 'date': file_date, 'size': file_size})

    processed_files = sorted(files, key=lambda x: x['date'], reverse=True)

    # zip driver
    print("\nStarting to zip please wait!")
    print("\n{:<30} {:<30} {:<20}".format('Filename', 'Date', 'Size(Bytes)\n'))
    zip_files(processed_files, entry_dir, exit_dir, zip_limit)


def main():
    # script docs
    print(' Auto Zipper '.center(85, '='))
    print("\nAutomatic file zipping tool: \
           \n- Ensure that all files you wish to bundle are in the correct entry \
           \n  directory and that both the entry/exit directories exist before continuing. \
           \n- Enter the correct directory paths and maxiumum zip file size in bytes when prompted. \
           \n- Directory Example Format: C:\\Users\\User\\Folder\n")

    # main driver
    zip_handler()


if __name__ == '__main__':
    main()
