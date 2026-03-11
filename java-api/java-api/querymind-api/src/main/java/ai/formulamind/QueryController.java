package ai.formulamind;

import org.springframework.web.bind.annotation.*;
import java.util.*;

@RestController
@RequestMapping("/api")
public class QueryController {

    private Map<String, List<Map<String, String>>> tables = new HashMap<>();

    @GetMapping("/ping")
    public Map<String, String> ping() {
        Map<String, String> response = new HashMap<>();
        response.put("status",  "running");
        response.put("engine",  "QueryMind v1.0");
        response.put("company", "4mulaMindAI");
        return response;
    }

    @PostMapping("/create")
    public Map<String, String> createTable(@RequestBody Map<String, Object> body) {
        String tableName = (String) body.get("table");
        tables.put(tableName, new ArrayList<>());
        Map<String, String> response = new HashMap<>();
        response.put("status",  "success");
        response.put("message", "Table '" + tableName + "' created!");
        return response;
    }

    @PostMapping("/insert")
    public Map<String, String> insert(@RequestBody Map<String, Object> body) {
        String tableName = (String) body.get("table");
        Map<String, String> row = (Map<String, String>) body.get("row");
        if (!tables.containsKey(tableName)) {
            Map<String, String> error = new HashMap<>();
            error.put("status",  "error");
            error.put("message", "Table not found!");
            return error;
        }
        tables.get(tableName).add(row);
        Map<String, String> response = new HashMap<>();
        response.put("status",  "success");
        response.put("message", "1 row inserted!");
        return response;
    }

    @GetMapping("/select/{table}")
    public Map<String, Object> select(@PathVariable String table) {
        Map<String, Object> response = new HashMap<>();
        if (!tables.containsKey(table)) {
            response.put("status",  "error");
            response.put("message", "Table not found!");
            return response;
        }
        response.put("status", "success");
        response.put("table",  table);
        response.put("rows",   tables.get(table));
        response.put("count",  tables.get(table).size());
        return response;
    }
}