
How to run this program:
    the main method is in yuntao_liang_hw5 329 lines. If you want to get data from website, type in 'python yuntao_liang_hw5.py --source=remote'. If you want to get data from local CSV files under the same directory, type in 'python yuntao_liang_hw5.py --source=local'. I already make the file under this directory, you can directly read them by '--source=local'. But if you delete these files, you have to get them from remote first and then get them from local. If you delete these files and want to read them from local, a alert message will be printed out.

Note:
    Because of request rating limitation, I set a time sleep inside the for loop, if you choose to get data from website, you need to wait for 2 - 3 minutes. I print some results while doing scraping to let users know the program is running.