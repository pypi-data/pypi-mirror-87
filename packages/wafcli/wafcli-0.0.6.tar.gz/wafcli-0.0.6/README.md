# T-Sec Web Application Firewall CLI
## Install
```bash
pip install wafcli
```

## Configure
### linux
~/.waf/waf.json   

### windows   
c:\Users\xxxx\.waf\waf.json

### Configure Items
- secret_id
- secret_key
- region
- edition (sparta-waf, clb-waf, cdn-waf)

**example**   
```json
{
    "secret_id": "aaaaa",
    "secret_key": "xxxx",
    "region": "ap-shanghai",
    "edition": "sparta-waf"
}
```
## Module
### domain
#### list
```bash
waf domain list 0 10
waf domain list --index 1 --count 20
```
either is ok

### custom_rule
#### list
```bash
waf custom_rule list example.com
```
#### copy
```bash
waf custom_rule copy example.com rule1 1.test.com,2.test.com
waf custom_rule copy example.com rule2 all
```

### ip
#### add
```bash
waf ip add global 2.2.2.2,1.1.1.1 --action 42
waf ip add www.test.com 3.3.3.3
```
#### list
#### delete
#### hits

### log
#### cursor
get cursor by from time
```bash
waf log cursor "2020-12-07 00:00:00"
```

#### export
export logs from cursor
```bash
waf log export 5FCDE1000005B5DB3A29F2EE000000000000 1000
```
