const express = require('express');
const axios = require('axios');
const session = require('express-session');

const app = express();
const PORT = process.env.PORT || 3000;
const FLASK_API_URL = 'http://127.0.0.1:5000/api';

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
  secret: 'senior_facility_secret_key',
  resave: false,
  saveUninitialized: true
}));

const requireAuth = (req, res, next) => {
  if (req.session && req.session.user) {
    return next();
  }
  res.redirect('/login');
};

app.use((req, res, next) => {
  res.locals.user = req.session.user || null;
  next();
});

//login
app.get('/login', (req, res) => {
  res.render('login', { error: null });
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  try {
    const response = await axios.post(`${FLASK_API_URL}/login`, { username, password });
    if (response.status === 200) {
      req.session.user = username;
      return res.redirect('/floors');
    }
  } catch (error) {
    res.render('login', { error: 'Invalid username or password.' });
  }
});

app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/login');
});

app.get('/', (req, res) => res.redirect('/floors'));

//floors
app.get('/floors', requireAuth, async (req, res) => {
  try {
    const response = await axios.get(`${FLASK_API_URL}/floors`);
    res.render('floors', { floors: response.data });
  } catch (err) {
    res.render('floors', { floors: [] });
  }
});

app.post('/floors/add', requireAuth, async (req, res) => {
  await axios.post(`${FLASK_API_URL}/floor`, req.body);
  res.redirect('/floors');
});

app.post('/floors/update', requireAuth, async (req, res) => {
  const { floor_id, floor_level, floor_name } = req.body;
  await axios.put(`${FLASK_API_URL}/floor/${floor_id}`, { floor_level, floor_name });
  res.redirect('/floors');
});

app.post('/floors/delete', requireAuth, async (req, res) => {
  const { floor_id } = req.body;
  await axios.delete(`${FLASK_API_URL}/floor/${floor_id}`);
  res.redirect('/floors');
});

//rooms 
app.get('/rooms', requireAuth, async (req, res) => {
  try {
    const [roomsRes, floorsRes] = await Promise.all([
      axios.get(`${FLASK_API_URL}/rooms`),
      axios.get(`${FLASK_API_URL}/floors`)
    ]);
    res.render('rooms', { rooms: roomsRes.data, floors: floorsRes.data });
  } catch (err) {
    res.render('rooms', { rooms: [], floors: [] });
  }
});

app.post('/rooms/add', requireAuth, async (req, res) => {
  await axios.post(`${FLASK_API_URL}/room`, req.body);
  res.redirect('/rooms');
});

app.post('/rooms/update', requireAuth, async (req, res) => {
  const { room_id, room_capacity, room_number, room_floor } = req.body;
  await axios.put(`${FLASK_API_URL}/room/${room_id}`, { room_capacity, room_number, room_floor });
  res.redirect('/rooms');
});

app.post('/rooms/delete', requireAuth, async (req, res) => {
  const { room_id } = req.body;
  await axios.delete(`${FLASK_API_URL}/room/${room_id}`);
  res.redirect('/rooms');
});


//residents
app.get('/residents', requireAuth, async (req, res) => {
  try {
    const [residentsRes, roomsRes] = await Promise.all([
      axios.get(`${FLASK_API_URL}/residents`),
      axios.get(`${FLASK_API_URL}/rooms`)
    ]);
    res.render('residents', { residents: residentsRes.data, rooms: roomsRes.data });
  } catch (err) {
    res.render('residents', { residents: [], rooms: [] });
  }
});

app.post('/residents/add', requireAuth, async (req, res) => {
  await axios.post(`${FLASK_API_URL}/resident`, req.body);
  res.redirect('/residents');
});

app.post('/residents/update', requireAuth, async (req, res) => {
  const { res_id, res_first_name, res_last_name, res_age, res_room } = req.body;
  await axios.put(`${FLASK_API_URL}/resident/${res_id}`, {
    res_first_name, res_last_name, res_age, res_room
  });
  res.redirect('/residents');
});

app.post('/residents/delete', requireAuth, async (req, res) => {
  const { res_id } = req.body;
  await axios.delete(`${FLASK_API_URL}/resident/${res_id}`);
  res.redirect('/residents');
});

app.listen(PORT, () => {
  console.log(`Sprint 2 Express Server running at http://localhost:${PORT}`);
});

