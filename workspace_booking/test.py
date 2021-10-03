def clean_room_name(*args, **kwargs):
    edit = kwargs['edit']
    print(edit)
    if edit is True:
        print('yes')
    else:
        print('no')


if __name__ == '__main__':
    clean_room_name(edit=False)
