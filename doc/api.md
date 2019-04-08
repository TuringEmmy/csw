在请求头里加入Authorization，并加上JWT 标注：

```angular2
fetch('api/user/1', {
  headers: {
    'Authorization': 'JWT ' + token
  }
})
```