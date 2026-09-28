import json
import sys
from client import ShamirSecretSharing

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "split_secret",
                        "description": "Split secret integer into n threshold shares with threshold k",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "secret_int": {"type": "integer"},
                                "k": {"type": "integer", "default": 3},
                                "n": {"type": "integer", "default": 5}
                            },
                            "required": ["secret_int"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "split_secret":
            shares = ShamirSecretSharing.split(args["secret_int"], args.get("k", 3), args.get("n", 5))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"shares": shares})}]}
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
