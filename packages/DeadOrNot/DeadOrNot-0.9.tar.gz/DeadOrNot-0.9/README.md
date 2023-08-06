# DeadOrNot

DeadOrNot is a Python program that parses a file for URLs and returns information about the HTTP status of those links to the command line 

![DeadOrNot](https://i.imgur.com/zw850Cd.png)

## Usage

Use the -h option to see information and other options
```bash
python deadOrNot.py -h
```
![DeadOrNot](https://i.imgur.com/pbr75wt.png)
Check and output URL status  
```bash
python deadOrNot.py *fileName*
```
![DeadOrNot](https://i.imgur.com/zw850Cd.png)
Use the -g/-good option to check and output live URL statuses
```bash
python deadOrNot.py  *fileName* -g
```
![DeadOrNot](https://i.imgur.com/Cr4lMpn.png)
Use the -d/-dead option to check and output dead or unknown URL statuses
```bash
python deadOrNot.py  *fileName* -d
```
![DeadOrNot](https://i.imgur.com/WcqMzVM.png)
Use the -in option to check URL statuses and output overall status information for all links in file
```bash
python deadOrNot.py *fileName* -in
```
![DeadOrNot](https://i.imgur.com/u3Ve1RD.png)
Use the -i option to compare links with a single link provided in a separate text file
If the links partially match, the corresponding link will be excluded from being checked
```bash
python deadOrNot.py 
```

## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See LICENSE for more information.
