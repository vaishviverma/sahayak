import { useState, useRef } from "react"; // React Hooks

import { useTheme } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";


import SendIcon from "@mui/icons-material/Send";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import DeleteIcon from "@mui/icons-material/Delete";
import { getSessionId } from "../../utils/session";




interface Message {
  text?: string;
  sender: "user" | "ai";
  fileName?: string;
}

export function Chatbot({ title = "Chat with Sahayak", subheader }: { title?: string; subheader?: string }) {
  const theme = useTheme();
  const [messages, setMessages] = useState<Message[]>([
    { text: "Hello! I'm Sahayak, your smart grocery assistant. How can I help you today?", sender: "ai" },
  ]);
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleSendMessage = async () => {
    setError(null);

    if (!input.trim() && !selectedFile) return;

    const newMessage: Message = { sender: "user", text: input || undefined, fileName: selectedFile?.name };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");

    try {
      const formData = new FormData();
      formData.append("message", input || "");
      formData.append("user_id", getSessionId());
      if (selectedFile) formData.append("file", selectedFile);

      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Error: ${response.statusText}`);

      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.response, sender: "ai" }]);
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (err) {
      setError("Error connecting to backend. Please check your server.");
      console.error("Error:", err);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <Card>
      <CardHeader title={title} subheader={subheader} />
      <Paper sx={{ p: 2, height: 400, overflowY: "auto", backgroundColor: theme.palette.background.default }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left", marginBottom: 8 }}>
            {msg.text && (
              <Paper sx={{ display: "inline-block", p: 1.5, backgroundColor: msg.sender === "user" ? theme.palette.primary.light : theme.palette.grey[300] }}>
                {msg.text}
              </Paper>
            )}
            {msg.fileName && (
              <Paper sx={{ p: 1.5, mt: 1, backgroundColor: theme.palette.grey[300] }}>
                📄 {msg.fileName}
              </Paper>
            )}
          </div>
        ))}
        {error && <Typography color="error">{error}</Typography>}
      </Paper>

      <Grid container spacing={1} alignItems="center" sx={{ padding: 1 }}>
        <Grid item xs>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </Grid>
        <Grid item>
          <input
            type="file"
            accept="application/pdf"
            style={{ display: "none" }}
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          <Button component="span" onClick={() => fileInputRef.current?.click()}>
            <AttachFileIcon />
          </Button>
        </Grid>
        <Grid item>
          <IconButton color="primary" onClick={handleSendMessage}>
            <SendIcon />
          </IconButton>
        </Grid>
      </Grid>

      {selectedFile && (
        <Paper sx={{ display: "flex", alignItems: "center", p: 1, mt: 1 }}>
          <Typography sx={{ flexGrow: 1 }}>📄 {selectedFile.name}</Typography>
          <IconButton onClick={handleRemoveFile}>
            <DeleteIcon />
          </IconButton>
        </Paper>
      )}
    </Card>
  );
}
