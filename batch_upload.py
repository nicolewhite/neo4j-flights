import sys

def batch_upload(batch, data, query, vars = None, batch_size = 1000):
    start = 0
    end = batch_size

    for i in range(len(data)):
        if(type(data[i]) is list):
            params = dict(zip(vars, data[i]))
        elif(type(data[i]) is dict):
            params = data[i]
        else:
            sys.exit("wat r u doing")

        if i in range(start, end):
            batch.append_cypher(query, params)
        else:
            batch.append_cypher(query, params)
            batch.run()
            batch.clear()
            print("Batch %s complete." % (end / batch_size))

            start = end + 1
            end = end + batch_size

    batch.run()
    batch.clear()
    print("Batch %s complete." % (end / batch_size))
    print("All done!\n")