# 保存日志

这段代码实现了一个日志文件备份和轮转系统，当文件大小超过限制时自动创建备份并清空原文件。核心功能如下：

1. **文件大小监控**：检查指定文件是否超过 10KB 的限制
2. **备份管理**：最多保留 5 个备份文件，采用轮转策略
3. **自动清理**：当备份数量达到上限时，自动删除最旧的备份
4. **压缩存储**：备份完成后将文件压缩为 tar.gz 格式以节省空间
5. **内容清空**：备份后清空原文件内容

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <time.h>
#include <libgen.h>

#define MAX_SIZE (10 * 1024)  // 10KB
#define MAX_BACKUPS 5

// 比较函数，用于排序文件时间
int compare_files(const void* a, const void* b) {
    struct stat st_a, st_b;
    stat(*(const char**)a, &st_a);
    stat(*(const char**)b, &st_b);
    return st_a.st_mtime - st_b.st_mtime;
}

// 检查文件大小并进行备份
int check_and_backup_file(const char* path) {
    struct stat st;

    // 检查文件是否存在
    if (stat(path, &st) != 0) {
        perror("stat failed");
        return -1;
    }

    // 检查文件大小是否超过限制
    if (st.st_size <= MAX_SIZE) {
        return 0; // 文件大小未超过限制
    }

    // 获取文件名和目录
    char* path_copy = strdup(path);
    char* dir = strdup(dirname(path_copy));
    char* base_name = basename(path);

    // 查找现有的备份文件
    DIR* dp = opendir(dir);
    if (!dp) {
        perror("opendir failed");
        free(path_copy);
        return -1;
    }

    char* backup_files[MAX_BACKUPS] = {0};
    int backup_count = 0;
    struct dirent* entry;

    char pattern[256];
    snprintf(pattern, sizeof(pattern), "%s__", base_name);

    while ((entry = readdir(dp)) != NULL && backup_count < MAX_BACKUPS) {
        if (strstr(entry->d_name, pattern) == entry->d_name) {
            char full_path[1024];
            snprintf(full_path, sizeof(full_path), "%s/%s", dir, entry->d_name);
            backup_files[backup_count++] = strdup(full_path);
        }
    }
    closedir(dp);
    free(path_copy);

    // 确定下一个备份编号
    int next_number = 1;
    if (backup_count >= MAX_BACKUPS) {
        // 按修改时间排序，找到最老的文件
        qsort(backup_files, backup_count, sizeof(char*), compare_files);
        char* oldest = backup_files[0];

        // 提取编号
        char* num_start = strrchr(oldest, '_') + 1;
        if (num_start) {
            next_number = atoi(num_start);
        }

        // 删除最老的备份文件
        remove(oldest);
        free(oldest);

        // 重新组织备份文件数组
        for (int i = 1; i < backup_count; i++) {
            backup_files[i - 1] = backup_files[i];
        }
        backup_count--;
    } else {
        // 查找最大的现有编号
        int max_number = 0;
        for (int i = 0; i < backup_count; i++) {
            char* num_start = strrchr(backup_files[i], '_') + 1;
            if (num_start) {
                int num = atoi(num_start);
                if (num > max_number) {
                    max_number = num;
                }
            }
            free(backup_files[i]);
        }
        next_number = max_number + 1;
    }

    // 创建新的备份文件名
    char new_name[1024];
    snprintf(new_name, sizeof(new_name), "%s/%s__%03d", dir, base_name, next_number);
    free(dir);

    // 执行备份
    char cmd[2048];
    snprintf(cmd, sizeof(cmd), "cp %s %s", path, new_name);
    if (system(cmd) != 0) {
        perror("Failed to execute backup command");
        return -1;
    }

    // 安全地清除 path 文件内容
    snprintf(cmd, sizeof(cmd), "echo -n > %s", path);
    if (system(cmd) != 0) {
        perror("Failed to clear file");
        return -1;
    }

    // 打包压缩（这里使用 tar.gz 作为示例）
    snprintf(cmd, sizeof(cmd), "tar -czf %s.tar.gz -C %s %s && rm %s",
             new_name, dirname(strdup(new_name)), basename(strdup(new_name)), new_name);
    if (system(cmd) != 0) {
        fprintf(stderr, "tar -czf failed\n");
        return -1;
    }
    printf("%s is backed up to %s.tar.gz\n", path, new_name);

    return 1;
}

// 使用示例
int main() {
    const char *filename = "test.log";
    int result = check_and_backup_file(filename);
    
    if (result == 1) {
        printf("backup success\n");
    } else if (result == 0) {
        printf("file size is normal\n");
    } else {
        printf("backup failed\n");
    }
    
    return 0;
}
```
