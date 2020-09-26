
ulong FUN_7f5bec178850(JNIEnv *jni_env,jclass param_2,undefined8 password_str)

{
  int *temp_ptr;
  jboolean exception_occured;
  int atoi_res;
  int parts_num;
  ulong return_value;
  long in_FS_OFFSET;
  code *malloc;
  code *free;
  code *memmove;
  code *memcmp;
  code *strlen;
  code *strtok;
  code *atoi;
  code *SHA256;
  code *mcrypt_module_open;
  code *mcrypt_generic_init;
  code *mdecrypt_generic;
  code *mcrypt_generic_end;
  jboolean local_1b7;
  bool good_password_flag;
  byte first_byte_of_password;
  int loop_counter1;
  int counter;
  int local_1ac;
  long split_part;
  jclass java_util_scanner;
  jmethodID scanner_string_constructor;
  jmethodID scanner_nextByte;
  jmethodID scanner_next;
  jfieldID FLAG_str;
  jobject scanner_obj;
  jobject rest_of_password;
  char *rest_of_password_bytearray;
  long rest_of_password_len;
  undefined8 password_ptr;
  long parts_memory;
  long local_148;
  long mcrypt_module;
  jobject flag_obj;
  jchar *flag_bytearray;
  undefined local_128 [16];
  undefined auStack280 [16];
  undefined8 local_108;
  undefined8 local_100;
  undefined8 local_f8;
  undefined8 local_f0;
  undefined8 local_e8;
  undefined8 local_e0;
  undefined8 local_d8;
  undefined8 local_d0;
  undefined8 local_c8;
  undefined8 local_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  long stack_cookie;
  uint temp_int_value;
  
  stack_cookie = *(long *)(in_FS_OFFSET + 0x28);
  local_d8 = 0x21f1e440a1d0a01;
  local_d0 = 0xe05050a08384407;
  local_c8 = 0x12291f130e056b19;
  local_c0 = 0x196b0809086b0e1f;
  local_b8 = 0x46070e0a0f050102;
  local_b0 = 0x121b04286b53595a;
  local_a8 = 0x436b0537184e4b51;
  local_a0 = 0xa07440a1d0a0127;
  local_98 = 0x502191f38440c05;
  local_90 = 0x180e126b3d42500c;
  local_88 = 0x1f130e056b184e6b;
  local_80 = 0x2576b04056b2b6b;
  local_78 = 0x2a272d6b551f0205;
  local_70 = 0x42436b2942436b2c;
  local_68 = 0xa07440a1d0a0127;
  local_60 = 0x502191f38440c05;
  local_58 = 0xa1d0a01276b500c;
  local_50 = 0x1f38440c050a0744;
  local_48 = 0x38236b500c050219;
  local_40 = 0x542e363a21314404;
  local_38 = 0x115c363d00124c38;
  local_30 = 0x6b0b4d293d0e;
  loop_counter1 = 0;
  while (loop_counter1 < 0xb0) {
    *(byte *)((long)&local_d8 + (long)loop_counter1) =
         *(byte *)((long)&local_d8 + (long)loop_counter1) ^ 0x6b;
    loop_counter1 = loop_counter1 + 1;
  }
                    /* FindClass java/util/Scanner  */
  java_util_scanner = (*(*jni_env)->FindClass)((JNIEnv *)jni_env,(char *)&local_d8);
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
                    /* GetMethodID(cls, "<init>", "(Ljava/lang/String;)V"); */
  scanner_string_constructor =
       (*(*jni_env)->GetMethodID)
                 ((JNIEnv *)jni_env,java_util_scanner,(char *)((long)&local_80 + 6),
                  (char *)((long)&local_a8 + 7));
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
                    /* nextByte()B */
  scanner_nextByte =
       (*(*jni_env)->GetMethodID)
                 ((JNIEnv *)jni_env,java_util_scanner,(char *)((long)&local_c8 + 2),
                  (char *)((long)&local_70 + 2));
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
                    /* next()Ljava/lang/String; */
  scanner_next = (*(*jni_env)->GetMethodID)
                           ((JNIEnv *)jni_env,java_util_scanner,(char *)((long)&local_88 + 4),
                            (char *)((long)&local_70 + 6));
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
                    /* FLAG Ljava/lang/String; */
  FLAG_str = (*(*jni_env)->GetStaticFieldID)
                       ((JNIEnv *)jni_env,param_2,(char *)((long)&local_78 + 5),
                        (char *)((long)&local_58 + 3));
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
                    /* Scanner scanner = new Scanner(password) */
  scanner_obj = (*(*jni_env)->NewObject)
                          ((JNIEnv *)jni_env,java_util_scanner,scanner_string_constructor,
                           password_str,(*jni_env)->NewObject);
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
  first_byte_of_password =
       (*(*jni_env)->CallByteMethod)
                 ((JNIEnv *)jni_env,scanner_obj,scanner_nextByte,(*jni_env)->CallByteMethod);
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
  rest_of_password =
       (*(*jni_env)->CallObjectMethod)
                 ((JNIEnv *)jni_env,scanner_obj,scanner_next,(*jni_env)->CallObjectMethod);
  exception_occured = (*(*jni_env)->ExceptionCheck)((JNIEnv *)jni_env);
  if (exception_occured != '\0') {
    return_value = 0;
    goto LAB_7f5bec17935c;
  }
  rest_of_password_bytearray =
       (*(*jni_env)->GetStringUTFChars)((JNIEnv *)jni_env,(jstring)rest_of_password,(jboolean *)0x0)
  ;
  rest_of_password_len = (*strlen)(rest_of_password_bytearray);
  password_ptr = (*malloc)(rest_of_password_len + 1);
  (*memmove)(password_ptr,rest_of_password_bytearray,rest_of_password_len + 1,password_ptr);
  parts_memory = (*malloc)(rest_of_password_len << 2);
  split_part = (*strtok)(password_ptr,(long)&local_80 + 1,strtok,password_ptr);
  counter = 0;
  while (split_part != 0) {
    temp_ptr = (int *)((long)counter * 4 + parts_memory);
    counter = counter + 1;
    atoi_res = (*atoi)(split_part);
    *temp_ptr = atoi_res;
                    /* split by @ */
    split_part = (*strtok)(0,(long)&local_80 + 1,strtok);
  }
  (*free)(password_ptr);
  parts_num = counter;
  local_1ac = counter;
  while (counter = counter + -1, 0 < counter) {
    *(int *)(parts_memory + (long)counter * 4 + -4) =
         *(int *)(parts_memory + (long)counter * 4 + -4) -
         *(int *)(parts_memory + (long)counter * 4);
    *(uint *)(parts_memory + (long)counter * 4) =
         (uint)first_byte_of_password ^ *(uint *)(parts_memory + (long)counter * 4);
  }
  counter = 0;
  while (counter < parts_num) {
    temp_int_value = *(uint *)(parts_memory + (long)counter * 4);
    *(uint *)(parts_memory + (long)counter * 4) =
         (temp_int_value << 5 | temp_int_value >> 0x1b) ^ 0xcafebabe;
    counter = counter + 1;
  }
  local_148 = (long)&local_48 + 6;
  parts_num = (*memcmp)(local_148,parts_memory,(long)parts_num << 2,local_148);
  good_password_flag = parts_num == 0;
  (*free)(parts_memory);
  if (good_password_flag == false) {
LAB_7f5bec179323:
    good_password_flag = false;
  }
  else {
    local_108 = 0xc1905790f237701c;
    local_100 = 0xb15eadcd797a210e;
    local_f8 = 0xf0338eb720ca51ab;
    local_f0 = 0xed281860633295c;
    local_e8 = 0x2f6f529a7fa2e318;
    local_e0 = 0xf9a5a567eaa76025;
    (*SHA256)(rest_of_password_bytearray,rest_of_password_len,local_128,rest_of_password_bytearray);
                    /* mcrypt_module_open("rijndael-128", NULL, "cbc", NULL); */
    mcrypt_module =
         (*mcrypt_module_open)((long)&local_c0 + 7,0,(long)&local_c0 + 3,0,mcrypt_module_open);
    if (((mcrypt_module == 0) ||
        (parts_num = (*mcrypt_generic_init)
                               (mcrypt_module,local_128,0x10,auStack280,mcrypt_generic_init),
        parts_num != 0)) ||
       (parts_num = (*mdecrypt_generic)(mcrypt_module,&local_108,0x30,mcrypt_module), parts_num != 0
       )) goto LAB_7f5bec179323;
    (*mcrypt_generic_end)(mcrypt_module);
    flag_obj = (*(*jni_env)->GetStaticObjectField)((JNIEnv *)jni_env,param_2,FLAG_str);
    flag_bytearray =
         (*(*jni_env)->GetStringCritical)((JNIEnv *)jni_env,(jstring)flag_obj,&local_1b7);
    counter = 0;
    while (counter < 0x19) {
      flag_bytearray[(long)counter + 5] = (short)*(char *)((long)&local_108 + (long)counter) & 0xff;
      counter = counter + 1;
    }
    (*(*jni_env)->ReleaseStringCritical)((JNIEnv *)jni_env,(jstring)flag_obj,flag_bytearray);
  }
  (*(*jni_env)->ReleaseStringUTFChars)
            ((JNIEnv *)jni_env,(jstring)rest_of_password,rest_of_password_bytearray);
  return_value = (ulong)good_password_flag;
LAB_7f5bec17935c:
  if (stack_cookie != *(long *)(in_FS_OFFSET + 0x28)) {
    return_value = func_0x7f5bec17854f();
  }
  return return_value;
}

