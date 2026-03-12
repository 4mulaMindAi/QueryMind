package ai.formulamind;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class QueryController {

    private Map<String, List<Map<String, String>>> tables  = new HashMap<>();
    private List<Map<String, String>>              history = new ArrayList<>();
    private Map<String, String>                    users   = new HashMap<>() {{
        put("admin", "querymind");
    }};

    @GetMapping("/ping")
    public Map<String, String> ping() {
        Map<String, String> res = new HashMap<>();
        res.put("status",  "running");
        res.put("engine",  "QueryMind v1.0");
        res.put("company", "4mulaMindAI");
        return res;
    }

    @PostMapping("/signup")
    public Map<String, String> signup(@RequestBody Map<String, Object> body) {
        String username = (String) body.get("username");
        String password = (String) body.get("password");
        String email    = (String) body.get("email");
        Map<String, String> res = new HashMap<>();
        if (username == null || username.isBlank()) {
            res.put("status",  "error");
            res.put("message", "Username is required!");
            return res;
        }
        if (password == null || password.length() < 6) {
            res.put("status",  "error");
            res.put("message", "Password must be at least 6 characters!");
            return res;
        }
        if (users.containsKey(username)) {
            res.put("status",  "error");
            res.put("message", "Username already exists!");
            return res;
        }
        users.put(username, password);
        res.put("status",  "success");
        res.put("message", "Account created successfully!");
        res.put("user",    username);
        return res;
    }

    @PostMapping("/login")
    public Map<String, String> login(@RequestBody Map<String, Object> body) {
        String username = (String) body.get("username");
        String password = (String) body.get("password");
        Map<String, String> res = new HashMap<>();
        if (users.containsKey(username) &&
            users.get(username).equals(password)) {
            res.put("status",  "success");
            res.put("message", "Login successful!");
            res.put("token",   "qm-" + username + "-token");
            res.put("user",    username);
        } else {
            res.put("status",  "error");
            res.put("message", "Invalid username or password!");
        }
        return res;
    }

    @PostMapping("/create")
    public Map<String, String> createTable(@RequestBody Map<String, Object> body) {
        String table = (String) body.get("table");
        tables.put(table, new ArrayList<>());
        logHistory("CREATE", table, "success");
        Map<String, String> res = new HashMap<>();
        res.put("status",  "success");
        res.put("message", "Table '" + table + "' created!");
        return res;
    }

    @PostMapping("/insert")
    public Map<String, String> insert(@RequestBody Map<String, Object> body) {
        String table = (String) body.get("table");
        Map<String, String> row = (Map<String, String>) body.get("row");
        if (!tables.containsKey(table)) {
            Map<String, String> err = new HashMap<>();
            err.put("status",  "error");
            err.put("message", "Table not found!");
            return err;
        }
        tables.get(table).add(row);
        logHistory("INSERT", table, "success");
        Map<String, String> res = new HashMap<>();
        res.put("status",  "success");
        res.put("message", "1 row inserted!");
        return res;
    }

    @GetMapping("/select/{table}")
    public Map<String, Object> select(@PathVariable String table) {
        Map<String, Object> res = new HashMap<>();
        if (!tables.containsKey(table)) {
            res.put("status",  "error");
            res.put("message", "Table not found!");
            return res;
        }
        logHistory("SELECT", table, "success");
        res.put("status", "success");
        res.put("table",  table);
        res.put("rows",   tables.get(table));
        res.put("count",  tables.get(table).size());
        return res;
    }

    @PostMapping("/delete")
    public Map<String, String> delete(@RequestBody Map<String, Object> body) {
        String table = (String) body.get("table");
        String key   = (String) body.get("key");
        String value = (String) body.get("value");
        if (!tables.containsKey(table)) {
            Map<String, String> err = new HashMap<>();
            err.put("status",  "error");
            err.put("message", "Table not found!");
            return err;
        }
        tables.get(table).removeIf(row -> value.equals(row.get(key)));
        logHistory("DELETE", table, "success");
        Map<String, String> res = new HashMap<>();
        res.put("status",  "success");
        res.put("message", "Row deleted!");
        return res;
    }

    @PostMapping("/update")
    public Map<String, String> update(@RequestBody Map<String, Object> body) {
        String table   = (String) body.get("table");
        String key     = (String) body.get("key");
        String value   = (String) body.get("value");
        Map<String, String> newData = (Map<String, String>) body.get("newData");
        if (!tables.containsKey(table)) {
            Map<String, String> err = new HashMap<>();
            err.put("status",  "error");
            err.put("message", "Table not found!");
            return err;
        }
        for (Map<String, String> row : tables.get(table)) {
            if (value.equals(row.get(key))) {
                row.putAll(newData);
            }
        }
        logHistory("UPDATE", table, "success");
        Map<String, String> res = new HashMap<>();
        res.put("status",  "success");
        res.put("message", "Row updated!");
        return res;
    }

    @GetMapping("/tables")
    public Map<String, Object> listTables() {
        Map<String, Object> res = new HashMap<>();
        res.put("status", "success");
        res.put("tables", new ArrayList<>(tables.keySet()));
        res.put("count",  tables.size());
        return res;
    }

    @GetMapping("/history")
    public Map<String, Object> getHistory() {
        Map<String, Object> res = new HashMap<>();
        res.put("status",  "success");
        res.put("history", history);
        return res;
    }

    private void logHistory(String operation, String table, String status) {
        Map<String, String> entry = new HashMap<>();
        entry.put("operation", operation);
        entry.put("table",     table);
        entry.put("status",    status);
        entry.put("time",      new Date().toString());
        history.add(entry);
    }
}
