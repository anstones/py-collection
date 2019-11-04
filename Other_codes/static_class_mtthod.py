class Dev():
    def __init__(self,devices):
        self.devices = devices

    @staticmethod
    def dev_format(devices):
        if not isinstance(devices, list):
            devices = [devices]
        tmp = []
        for dev in devices:
            if dev == "":
                continue
            if len(dev) == len("0000000000_001122334455"):
                tmp.append(dev.lower())  # mac地址小写
            else:
                tmp.append(dev)
        return tmp



d = Dev("MMM0000000_001122334455")
print(d.devices)
new_dev = Dev.dev_format(d.devices) # 静态方法不会随类初始化
print(d.devices)
print(new_dev)