gb = GB(desc="Put last even in LAST_OP key")
gb.foreach(lambda x: execute('SET', "LAST_OP", x))
gb.register('*', mode='sync', readValue=True)
