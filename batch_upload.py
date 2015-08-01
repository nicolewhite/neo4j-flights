import sys

def batch_upload(graph, data, query, vars = None, batch_size = 1000):
    curr_batch_size = 0
    curr_batch_count = 1
    tx = graph.cypher.begin()

    for i in range(len(data)):
        if(type(data[i]) is list):
            params = dict(zip(vars, data[i]))
        elif(type(data[i]) is dict):
            params = data[i]
        else:
            sys.exit("wat r u doing")

        tx.append(query, params)

        curr_batch_size += 1
        if (curr_batch_size == batch_size):
            tx.process()
            tx.commit()

            print("Batch %s complete." % curr_batch_count)
            curr_batch_count += 1
            curr_batch_size = 0

            tx = graph.cypher.begin()

    tx.process()
    tx.commit()
    print("Batch %s complete." % curr_batch_count)
    print("All done!\n")
