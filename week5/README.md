# 要求三：SQL CRUD

> 利⽤要求⼆建立的資料庫和資料表，寫出能夠滿⾜以下要求的 SQL 指令：

- ## 使⽤ INSERT 指令新增⼀筆資料到 member 資料表中，這筆資料的 username 和password 欄位必須是 test。  
接著繼續新增⾄少 4 筆隨意的資料。  

  ![insert](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/insert.png)
- ## 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料。  

  ![select](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/select.png)
- ## 使⽤ SELECT 指令取得所有在 member 資料表中的會員資料，並按照 time 欄位，由近到遠排序。  

  ![order_by](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/order_by.png)
- ## 使⽤ SELECT 指令取得 member 資料表中第 2 ~ 4 共三筆資料，並按照 time 欄位，由近到遠排序。  
( 並非編號 2、3、4 的資料，⽽是排序後的第 2 ~ 4 筆資料 )  

  ![limit](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/limit.png)
- ## 使⽤ SELECT 指令取得欄位 username 是 test 的會員資料。  

  ![where](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/where.png)
- ## 使⽤ SELECT 指令取得欄位 username 是 test、且欄位 password 也是 test 的資料。  

  ![and](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/and.png)
- ## 使⽤ UPDATE 指令更新欄位 username 是 test 的會員資料，將資料中的 name 欄位改成 test2。   

  ![update](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/update.png)

---

# 要求四：SQL Aggregate Functions

> 利⽤要求⼆建立的資料庫和資料表，寫出能夠滿⾜以下要求的 SQL 指令：

- ## 取得 member 資料表中，總共有幾筆資料 ( 幾位會員 )。  
  ![count](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/count.png)
- ## 取得 member 資料表中，所有會員 follower_count 欄位的總和。  
  ![sum](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/sum.png)
- ## 取得 member 資料表中，所有會員 follower_count 欄位的平均數。  
  ![avg](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/avg.png)

---

# 要求五：SQL JOIN (Optional)

> 在資料庫中，建立新資料表紀錄留⾔資訊，取名字為 message。資料表中必須包含以
> 下欄位設定：

| 欄位名稱   | 資料型態     | 額外設定                                    | 用途說明       |
| ---------- | ------------ | ------------------------------------------- | -------------- |
| id         | bigint       | 主鍵、自動遞增                              | 獨立編號       |
| member_id  | bigint       | 不可為空值<br>外鍵對應 member 資料表中的 id | 留言者會員編號 |
| content    | varchar(255) | 不可為空值                                  | 留言內容       |
| like_count | int unsigned | 不可為空值，預設為 0                        | 按讚的數量     |
| time       | datetime     | 不可為空值，預設為當前時間                  | 留言時間       |

- ## 使⽤ SELECT 搭配 JOIN 語法，取得所有留⾔，結果須包含留⾔者會員的姓名。  

  ![inner_join](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/inner_join.png)
- ## 使⽤ SELECT 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔，資料中須包含留⾔者會員的姓名。  
  
  ![inner_join2](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/inner_join2.png)
- ## 使⽤ SELECT、SQL Aggregate Functions 搭配 JOIN 語法，取得 member 資料表中欄位 username 是 test 的所有留⾔平均按讚數。  
  
  ![avg](https://raw.githubusercontent.com/TWjohnwang/WeHelp.github.io/main/week5/img/avg2.png)
