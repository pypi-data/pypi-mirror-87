from carota import carota
import argparse

# Arguments
ENCLOSER = ''
DELIMITER = ','
ROWS = 10
TEXT = 'index; uuid; firstname; lastname; int::start=18,end=95; date::delta=365'
OUTPUT = ''
CHUNK_SIZE = 100000

def getArgs():
    """ Get command line args """
    parser = argparse.ArgumentParser(description='Generate data')
    parser.add_argument("-r", "--rows", dest='ROWS',
                        default=ROWS, help='Number of rows, default <' + str(ROWS) + '>')
    parser.add_argument("-t", "--text", dest='TEXT',
                        default=TEXT, help='Text, default <' + TEXT + '>')
    parser.add_argument("-d", "--delimiter", dest='DELIMITER',
                        default=DELIMITER, help='Delimiter, default <' + DELIMITER + '>')
    parser.add_argument("-e", "--encloser", dest='ENCLOSER',
                        default=ENCLOSER, help='Encloser, default <' + ENCLOSER + '>')
    parser.add_argument("-o", "--output", dest='OUTPUT',
                        default=OUTPUT, help='output filepath, default =  STDOUT')
    parser.add_argument("-c", "--chunck-size", dest='CHUNK_SIZE',
                        default=CHUNK_SIZE, help='count of rows to write to file at a time, default <' + str(CHUNK_SIZE) + '>')
    return parser.parse_args()



def main():
    options = getArgs()

    # trick to allow passing tab as a delimiter   
    options.DELIMITER = '\t' if options.DELIMITER == '\\t' else options.DELIMITER

    iterator = carota.carota(rows = int(options.ROWS), 
                        text = options.TEXT, 
                        delimiter = options.DELIMITER, 
                        encloser = options.ENCLOSER)
    
    l = []
    hasMore = True
    sum = 0

    if options.OUTPUT == '':
        for v in iterator:
            print(v)
    else:
        # create/override file
        with open(options.OUTPUT, 'w') as f:
            pass

        while hasMore:
            for i in range(int(options.CHUNK_SIZE)):
                try:
                    l.append(next(iterator))
                    
                except StopIteration:
                    hasMore = False
                    break
            

            with open(options.OUTPUT, 'a') as f:
                f.write('\n'.join(l) + '\n')


            sum = sum + i + 1
            print("written lines: " + str(sum))
            l=[]
            
if __name__ == "__main__":
    main()