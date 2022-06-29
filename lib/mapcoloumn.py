
def mapColumn(column: str, func):
    def wrapper(row):
        print(row)
        row[column] = row[column].map(func)
        return row

    return wrapper