
# ==============================================================================
#    OBJEKT ZA DELO Z MICRA DATOTEKAMI ".jda"
#
#    Avtor:   JAZON
#    Datum:   4-12-2020
#    Verzija: 1.2
# ==============================================================================

import datetime

class Jda2dtv:
    # Objekt za pretvorbo "jda" datoteke v "dJ" in "dtv" datoteko
    def __init__(self):
        self.chanels = []
        self.ch_sizes = []
        self.records = []

    def load_file(self, file_name):
        # Glavna funcija za pretvorbo. Vraca: true/false OK/neuspeh
        inx = file_name.find('.')
        self.raw_file_name = file_name[:inx]
        with open(file_name, "rb") as file:
            self.buff = file.read()
        lt = self.buff.decode('iso-8859-2')
        self.data_index = lt.find('$HEADER END')    # + cr, lf 0
        self.header = lt[:self.data_index+11]
        while self.buff[self.data_index] != 0:
            self.data_index += 1
        self.data_index += 1
        self.convert_header()
        type = self.dheader['FILE_TYPE']
        if type == '0' or type == '1':
            raise Exception("Napaka 3: Datoteki tipa 0 in 1 nista podprti")
        self.file_type_23()

    def convert_header(self):
        # Pretvorba headerja v dictionary
        self.dheader = {}
        for line in self.header.splitlines():
            inx = line.find('=')
            if inx > 0:
                key = line[:inx]
                val = line[inx+1:]
                self.dheader[key] = val

    def file_type_23(self):
        # Kreira listo rekordov iz podatkov datoteke tipa 2 in 3
        self.get_chan_data()
        self.records = []
        for i in range(self.no_records):
            self.records.append(self.get_record())

    def buff_num(self, n_bytes):
        # Pretvorba n_bytes iz buff v cifro + premakne pointer
        x = 0
        for i in range(n_bytes):
            bi = n_bytes - i - 1
            x += (self.buff[self.data_index] << (8*bi))
            self.data_index += 1
        return x

    def buff_chan(self):
        ''' Pretvori no_data_bytes: izpod pointerja v listo bitnih vrednosti kanalov
            Primer:
            ch_sizes = [15, 6] -> dolzina podatkov v rekordu je 3 byti

            bits:     23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
            ch0bits:                                                    5 4 3 2 1 0
            ch1bits:        15 14 13 12 11 10  9  8  7  6  5  4 3 2 1 0

            + premakne pointer
            return: listo bitnih vrednosti kanalov
        '''
        bits = 0
        for i in range(self.no_data_bytes):
            bits = bits << 8
            bits += self.buff[self.data_index + i]
        chans = []
        for no_bits in reversed(self.ch_sizes):
            mask = (2 ** no_bits) - 1
            chans.append(bits & mask)
            bits = bits >> no_bits
        self.data_index += self.no_data_bytes
        chans.reverse()
        return chans

    def get_no_records(self):
        # Izmeri stevilo rekordov
        no_data_bytes = sum(self.ch_sizes) / 8            # Stevilo bytov podatkov kanalov
        if(sum(self.ch_sizes) % 8) != 0:
            no_data_bytes += 1
        self.no_data_bytes = int(no_data_bytes)
        record_size = self.no_data_bytes + 4                   # Stevilo bytov za cas
        data_size = len(self.buff) - self.data_index
        if (data_size % record_size) != 0:
            raise Exception("Napaka 2: Nepravilna velikost podatkov")
        self.no_records = int(data_size / record_size)

    def get_raw_record(self):
        # Iz buffra vzame en record - vrne surove cifre izpod pointerja premakne pointer v bufru
        time = self.buff_num(4)
        ch_data = self.buff_chan()
        return time, ch_data

    def get_record(self):
        # Vrne formatiran preracunan rekord v listo: [cas, kanal, kanal, ... ]
        time, data = self.get_raw_record()
        record = [self.num_time(time)]
        for i,chan in enumerate(self.chanels):
            tmin = float(chan['MIN'])
            tmax = float(chan['MAX'])
            max_val = (2 ** self.ch_sizes[i]) - 1
            val = int(data[i]) * (tmax - tmin) / max_val + tmin
            format = self.chanels[i]['FOR']
            sval = self.chanels[i]['FOR'] % val
            record.append(sval)
        return record

    def num_time(s, num):
        # Pretvorba MICRA time v PYTHON datetime
        dni = int(num / 86400)
        leto = int(dni / 372) + 2000
        dni %= 372
        mesec = int(dni / 31) + 1
        date = dni % 31 + 1
        num %= 86400
        hours = int(num / 3600)
        num %= 3600
        minutes = int(num / 60)
        seconds = num % 60
        time = datetime.datetime(leto, mesec, date, hours, minutes, seconds)
        return time

    def get_chan_data(self):
        # Ekstrahira podatke kanalov: Prisotnost, NAME, UNIT, FOR, MIN, MAX
        self.chan_mask = 0
        self.chanels = []
        lb = self.dheader['CH_BITS']
        if lb[-1] == ',':
            lb = lb[:-1]
        self.ch_sizes = lb.split(",")
        self.ch_sizes = [int(i) for i in self.ch_sizes]
        for ch in range(8):
            key = "CH" + str(ch) + "_NAME"
            if key in self.dheader:
                self.chan_mask |= 0x01 << ch
                chan = {}
                chan['INDEX'] = ch
                chan['NAME'] = self.dheader[key]
                key = "CH" + str(ch) + "_UNIT"
                chan['UNIT'] = self.dheader[key]
                key = "CH" + str(ch) + "_FOR"
                chan['FOR'] = self.dheader[key]
                key = "CH" + str(ch) + "_MIN"
                chan['MIN'] = self.dheader[key]
                key = "CH" + str(ch) + "_MAX"
                chan['MAX'] = self.dheader[key]
                self.chanels.append(chan)
        self.get_no_records()

    def write_dJ_file(self, file_name=''):
        # Kreiranje dJ datoteke
        if file_name == '':
            file_name = self.raw_file_name + '.dJ'
        self.tex = ''
        self.add_line('NO_CHAN=%d' % len(self.chanels))
        for i, chan in enumerate(self.chanels):
            self.add_line('CHAN_NAME%d=%s'   % (i, chan['NAME']))
            self.add_line('CHAN_UNIT%d=%s'   % (i, chan['UNIT']))
            self.add_line('CHAN_FORMAT%d=%s' % (i, chan['FOR']))
            self.add_line('CHAN_MIN%d=%s'    % (i, chan['MIN']))
            self.add_line('CHAN_MAX%d=%s'    % (i, chan['MAX']))
        self.add_line('PROJECT=')
        self.add_line('$DATA')
        for record in self.records:
            for i,ch in enumerate(record):
                if i == 0:
                    lt = record[0].strftime("%Y/%m/%d %H:%M:%S")
                else:
                    if i > 1:
                        lt += ',' + record[i]
                    else:
                        lt += ', ' + record[i]
            self.add_line(lt + ',')
        with open(file_name, "w", encoding='iso-8859-2') as text_file:
            text_file.write(self.tex)

    def write_dtv_files(self, file_name=''):
        # Kreiranje Henrik (dtv) datoteke
        # Datoteke dobijo ime  file_name_(ImeKanala).dtv
        # Če parametra ni je file_name ime izvorne datoteke
        if file_name == '':
            file_name = self.raw_file_name
        for i, chan in enumerate(self.chanels):
            self.tex = '\n\n' + chan['UNIT'] + '\n' * 8
            for record in self.records:
                self.add_line(record[0].strftime("%d/%m/%Y %H:%M:%S") + ',' + record[i+1])
            fname = file_name + '_' + chan['NAME'] + '.dtv'
            with open(fname, "w", encoding='iso-8859-2') as text_file:
                text_file.write(self.tex)

    def add_line(self, text):
        self.tex += text + '\n'
