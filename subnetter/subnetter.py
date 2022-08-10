class Subnetter:

    def __init__(self, ip, mask):
        self.ip = ip
        self.mask = mask.strip('/')
        self.ipChecker()
        self.maskChecker()

    def cidr_to_bin(self):
        li = []
        for i in range(int(int(self.mask) / 8)):
            li.append('11111111')
        remain = int(self.mask) % 8
        if remain > 0:
            li.append('1' * remain + '0' * (8 - remain))
        while len(li) < 4:
            li.append('00000000')
        return '.'.join(li)

    def binary(self):
        bin_ip = '.'.join(
            ['{0:08b}'.format(int(x)) for x in self.ip.split('.')])
        try:
            if 0 <= int(self.mask) <= 32:
                bin_mask = self.cidr_to_bin()
                return bin_ip, bin_mask
            else:
                return bin_ip, None
        except ValueError:
            try:
                bin_mask = '.'.join(
                    ['{0:08b}'.format(int(x)) for x in self.mask.split('.')])
            except ValueError:
                return bin_ip, None
            return bin_ip, bin_mask

    def ander(self):
        li = []
        bin_ip, bin_mask = self.binary()
        ip_li = list(bin_ip)
        mask_li = list(bin_mask)
        for i in range(35):
            if ip_li[i] == mask_li[i]:
              li.append(ip_li[i])
            else:
              li.append('0')
        return ''.join(li), bin_mask

    def network(self):
        bin_net, bin_mask = self.ander()
        net = '.'.join([str(int(x, 2)) for x in bin_net.split('.')])
        sub = '.'.join([str(int(x, 2)) for x in bin_mask.split('.')])
        return net, sub

    def first(self):
        if 31 <= int(self.cidr()) <= 32:
            return 'NA'
        else:
            net, _ = self.network()
            return '.'.join([x if i != 3 else str(
                int(x) + 1) for i, x in enumerate(net.split('.'))])

    def broadcast(self):
        li = []
        net, sub = self.network()
        net_li = net.split('.')
        sub_li = sub.split('.')
        for i in range(4):
            if sub_li[i] == '255':
                li.append(net_li[i])
            else:
                dif = int(255) - int(sub_li[i])
                li.append(str(int(net_li[i]) + dif))
        return '.'.join(li)

    def last(self):
        if 31 <= int(self.cidr()) <= 32:
            return 'NA'
        else:
            broadcast = self.broadcast()
            return '.'.join([x if i != 3 else str(
                int(x) - 1) for i, x in enumerate(broadcast.split('.'))])

    def hosts(self):
        _, sub = self.binary()
        return 2 ** sub.count('0')

    def wildcard(self):
        li = []
        _, sub = self.binary()
        for i in sub.split('.'):
            li.append(''.join(['1' if x == '0' else '0' for x in i]))
        return '.'.join([str(int(x, 2)) for x in li])

    def cidr(self):
        _, sub = self.binary()
        return sub.count('1')

    def maskChecker(self):
        _, sub = self.binary()
        if sub is None:
            raise ValueError('Subnet is Invalid')
        mask = ''.join([x for x in sub.split('.')])
        if len(mask) != 32:
            raise ValueError('Subnet is Invalid')
        else:
            foundZero = False
            for bit in mask:
              try:
                  int(bit) + 1
              except ValueError:
                  raise ValueError('Subnet is Invalid')
              if foundZero:
                  if int(bit) == 0:
                      pass
                  else:
                      raise ValueError('Subnet is Invalid')
              else:
                  if int(bit) == 0:
                      foundZero = True
                  elif  int(bit) > 1:
                      raise ValueError('Subnet is Invalid')

    def ipChecker(self):
        octets = self.ip.split('.')
        if len(octets) != 4:
            raise ValueError('IP is Invalid')
        for idx, octet in enumerate(octets):
            try:
                if not 0 <= int(octet) <= 255:
                    raise ValueError('IP is Invalid')
            except ValueError:
                raise ValueError('IP is Invalid')

