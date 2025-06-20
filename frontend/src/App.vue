<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Student Concentration Tracker</h1>
              <p class="text-sm text-gray-600">Real-time emotion and concentration monitoring</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 rounded-full" :class="connectionStatus ? 'bg-green-500' : 'bg-red-500'"></div>
              <span class="text-sm text-gray-600">{{ connectionStatus ? 'Connected' : 'Disconnected' }}</span>
            </div>
            
            <button 
              @click="toggleCamera" 
              :class="cameraActive ? 'btn-danger' : 'btn-success'"
              :disabled="loading"
            >
              <span v-if="loading">Loading...</span>
              <span v-else>{{ cameraActive ? 'Stop Camera' : 'Start Camera' }}</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Students</p>
              <p class="text-2xl font-bold text-gray-900">{{ statistics.total_faces }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Avg Concentration</p>
              <p class="text-2xl font-bold" :class="getConcentrationClass(statistics.avg_concentration)">
                {{ statistics.avg_concentration.toFixed(1) }}%
              </p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Detections</p>
              <p class="text-2xl font-bold text-gray-900">{{ statistics.total_detections }}</p>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Session Time</p>
              <p class="text-2xl font-bold text-gray-900">{{ formatSessionTime() }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Feed and Face Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Live Camera Feed -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold text-gray-900">Live Camera Feed</h2>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
                <span class="text-sm text-gray-600">LIVE</span>
              </div>
            </div>
            
            <div class="aspect-video bg-gray-900 rounded-lg overflow-hidden relative">
              <img 
                v-if="currentFrame" 
                :src="`data:image/jpeg;base64,${currentFrame}`" 
                alt="Live Feed"
                class="w-full h-full object-cover"
              />
              <div v-else class="flex items-center justify-center h-full">
                <div class="text-center text-gray-400">
                  <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 012 2z"></path>
                  </svg>
                  <p>{{ cameraActive ? 'Waiting for camera feed...' : 'Camera is off' }}</p>
                </div>
              </div>
              
              <!-- Current Detections Overlay -->
              <div v-if="currentDetections.length > 0" class="absolute top-4 right-4">
                <div class="bg-black bg-opacity-75 text-white px-3 py-2 rounded-lg">
                  <p class="text-sm">{{ currentDetections.length }} face(s) detected</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Emotion Distribution Chart -->
        <div class="card">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Emotion Distribution</h3>
          <div class="space-y-3">
            <div v-for="(count, emotion) in statistics.emotion_distribution" :key="emotion" class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span :class="`emotion-badge emotion-${emotion}`">{{ emotion }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <div class="w-20 bg-gray-200 rounded-full h-2">
                  <div 
                    class="bg-primary-600 h-2 rounded-full transition-all duration-300" 
                    :style="{ width: `${(count / Math.max(...Object.values(statistics.emotion_distribution))) * 100}%` }"
                  ></div>
                </div>
                <span class="text-sm text-gray-600 w-8">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tracked Students -->
      <div class="mt-8">
        <div class="card">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-semibold text-gray-900">Tracked Students</h2>
            <button @click="exportData" class="btn-secondary">
              <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              Export Data
            </button>
          </div>
          
          <div v-if="faces.length === 0" class="text-center py-12">
            <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <p class="text-gray-600">No students detected yet</p>
            <p class="text-sm text-gray-500 mt-1">Start the camera to begin tracking</p>
          </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">            <div 
              v-for="face in faces" 
              :key="face.face_id" 
              class="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" 
              @click="openStudentHistory(face.face_id)"
            >              <!-- Student Image -->
              <div class="w-full h-32 bg-gray-200 rounded-lg mb-4 flex items-center justify-center overflow-hidden relative">
                <img 
                  v-if="getFaceImage(face.face_id)" 
                  :src="`data:image/jpeg;base64,${getFaceImage(face.face_id)}`"
                  class="object-cover w-full h-full student-face-image" 
                  alt="Student face"
                  @error="handleImageError($event, face.face_id)"
                />
                <svg v-else class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
                
                <!-- Student ID Overlay -->
                <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-xs py-1 px-2">
                  ID: {{ face.face_id.slice(-6) }}
                </div>
              </div>
              
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-gray-900">Student #{{ face.face_id.slice(-4) }}</span>
                  <span class="text-xs text-gray-500">{{ face.total_detections }} detections</span>
                </div>
                
                <div class="flex items-center justify-between">
                  <span :class="`emotion-badge emotion-${face.dominant_emotion}`">{{ face.dominant_emotion }}</span>
                  <span class="text-sm font-medium" :class="getConcentrationClass(face.avg_concentration)">
                    {{ face.avg_concentration.toFixed(1) }}%
                  </span>
                </div>
                
                <div class="text-xs text-gray-500">
                  <p>First seen: {{ formatTime(face.first_seen) }}</p>
                  <p>Last seen: {{ formatTime(face.last_seen) }}</p>
                </div>
                
                <!-- Concentration Progress Bar -->
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300" 
                    :class="getConcentrationBarClass(face.avg_concentration)"
                    :style="{ width: `${face.avg_concentration}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Student History Modal -->
      <div v-if="showHistoryModal" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="showHistoryModal = false"></div>
        <div class="bg-white rounded-lg shadow-lg p-6 max-w-lg w-full relative z-10">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">Student History - ID: {{ selectedFaceId ? selectedFaceId.slice(-6) : '' }}</h3>
            <button @click="showHistoryModal = false" class="text-gray-500 hover:text-gray-700">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <div v-if="!studentHistory[selectedFaceId] || studentHistory[selectedFaceId].length === 0" class="text-center py-12">
            <p class="text-gray-600">No history available for this student</p>
          </div>
          
          <div v-else>
            <!-- Student Image -->
            <div class="flex items-center mb-4">
              <div class="w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center overflow-hidden">
                <img 
                  v-if="getFaceImage(selectedFaceId)" 
                  :src="`data:image/jpeg;base64,${getFaceImage(selectedFaceId)}`"
                  class="object-cover w-full h-full"
                  alt="Student face"
                />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-900">Student #{{ selectedFaceId ? selectedFaceId.slice(-4) : '' }}</p>
                <p class="text-xs text-gray-500">{{ studentHistory[selectedFaceId] ? studentHistory[selectedFaceId].length : 0 }} data points</p>
              </div>
            </div>            <!-- History Chart -->
            <div class="mb-6 bg-gray-50 p-3 rounded-lg">
              <h4 class="text-sm font-medium text-gray-700 mb-2">Concentration Over Time</h4>
              <div class="h-48 relative chart-container">
                <canvas id="historyChart" width="400" height="200" style="display: block;"></canvas>
              </div>
            </div>
            
            <!-- History Table -->
            <div class="max-h-60 overflow-y-auto">
              <table class="min-w-full bg-white rounded-lg">
                <thead>
                  <tr class="bg-gray-100 text-gray-700">
                    <th class="py-2 px-4 text-left text-xs font-medium">Time</th>
                    <th class="py-2 px-4 text-left text-xs font-medium">Emotion</th>
                    <th class="py-2 px-4 text-left text-xs font-medium">Concentration</th>
                  </tr>
                </thead>
                <tbody class="text-gray-600">
                  <tr v-for="(entry, index) in [...studentHistory[selectedFaceId]].reverse()" :key="index" class="hover:bg-gray-50 border-t border-gray-100">
                    <td class="py-2 px-4 text-xs">{{ new Date(entry.timestamp).toLocaleTimeString() }}</td>
                    <td class="py-2 px-4">
                      <span :class="`emotion-badge emotion-${entry.emotion}`">{{ entry.emotion }}</span>
                    </td>
                    <td class="py-2 px-4">
                      <span :class="getConcentrationClass(entry.concentration)" class="text-xs font-medium">{{ entry.concentration.toFixed(1) }}%</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    // Reactive data
    const faces = ref([])
    const statistics = reactive({
      total_faces: 0,
      total_detections: 0,
      avg_concentration: 0,
      emotion_distribution: {}
    })
    const currentFrame = ref(null)
    const currentDetections = ref([])
    const cameraActive = ref(false)
    const connectionStatus = ref(false)
    const loading = ref(false)
    const sessionStartTime = ref(new Date())
    const faceImagesHistory = reactive({}) // Store persistent face images
    
    // Student history tracking
    const studentHistory = reactive({}) // Track emotion and concentration history
    const selectedFaceId = ref(null) // Currently selected face for history view
    const showHistoryModal = ref(false) // Control history modal visibility
    
    // WebSocket connection
    let ws = null
      // API base URL
    const API_BASE = 'http://localhost:8000'
    
    // Throttle saving to localStorage to prevent performance issues
    let saveTimeoutId = null
    const saveFaceImagesHistoryThrottled = () => {
      if (saveTimeoutId) clearTimeout(saveTimeoutId)
      saveTimeoutId = setTimeout(() => {
        saveFaceImagesHistory()
      }, 2000) // Save every 2 seconds at most
    }

    // Save face images to localStorage
    const saveFaceImagesHistory = () => {
      try {
        localStorage.setItem('faceImagesHistory', JSON.stringify(faceImagesHistory))
      } catch (error) {
        console.error('Error saving face images to localStorage:', error)
      }
    }

    // Load face images from localStorage
    const loadFaceImagesHistory = () => {
      try {
        const savedImages = localStorage.getItem('faceImagesHistory')
        if (savedImages) {
          const parsedImages = JSON.parse(savedImages)
          Object.keys(parsedImages).forEach(key => {
            faceImagesHistory[key] = parsedImages[key]
          })
          console.log('Loaded face images from localStorage:', Object.keys(faceImagesHistory).length)
        }
      } catch (error) {
        console.error('Error loading face images from localStorage:', error)
      }
    }

    // Handle image loading error
    const handleImageError = (event, faceId) => {
      console.error(`Error loading image for face ID ${faceId}`)
      // Remove invalid image from history
      if (faceImagesHistory[faceId]) {
        delete faceImagesHistory[faceId]
        saveFaceImagesHistory()
      }
    }
    
    // Initialize WebSocket connection
    const initWebSocket = () => {
      ws = new WebSocket('ws://localhost:8000/ws')
      
      ws.onopen = () => {
        connectionStatus.value = true
        console.log('Connected to WebSocket server')
      }
      
      ws.onclose = () => {
        connectionStatus.value = false
        console.log('Disconnected from WebSocket server')
        // Attempt to reconnect after 3 seconds
        setTimeout(initWebSocket, 3000)
      }
        ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          if (message.type === 'detection_update') {
            const data = message.data
            if (data.frame) {
              currentFrame.value = data.frame
            }
            if (data.detections) {
              currentDetections.value = data.detections
              
              // Store face images in history for persistence
              data.detections.forEach(detection => {
                if (detection.face_id && detection.face_image) {
                  faceImagesHistory[detection.face_id] = detection.face_image
                  
                  // Record history data for each detection
                  if (detection.emotion && detection.concentration !== undefined) {
                    if (!studentHistory[detection.face_id]) {
                      studentHistory[detection.face_id] = []
                    }
                    // Add the current detection to history with timestamp
                    studentHistory[detection.face_id].push({
                      timestamp: new Date(),
                      emotion: detection.emotion,
                      concentration: detection.concentration
                    })
                    
                    // Limit history size to prevent memory issues (keep last 100 entries)
                    if (studentHistory[detection.face_id].length > 100) {
                      studentHistory[detection.face_id] = studentHistory[detection.face_id].slice(-100)
                    }
                  }
                }
              })
              
              // Save to localStorage (throttled to avoid performance issues)
              if (data.detections.length > 0) {
                saveFaceImagesHistoryThrottled()
              }
            }
            if (data.statistics) {
              Object.assign(statistics, data.statistics)
            }
            // Refresh faces list
            fetchFaces()
          }
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
    }
    
    // Fetch faces from API
    const fetchFaces = async () => {
      try {
        const response = await axios.get(`${API_BASE}/faces`)
        faces.value = response.data.faces
      } catch (error) {
        console.error('Error fetching faces:', error)
      }
    }
    
    // Fetch statistics
    const fetchStatistics = async () => {
      try {
        const response = await axios.get(`${API_BASE}/statistics`)
        Object.assign(statistics, response.data)
      } catch (error) {
        console.error('Error fetching statistics:', error)
      }
    }
    
    // Toggle camera
    const toggleCamera = async () => {
      loading.value = true
      try {
        if (cameraActive.value) {
          await axios.post(`${API_BASE}/camera/stop`)
          cameraActive.value = false
          currentFrame.value = null
          currentDetections.value = []
        } else {
          await axios.post(`${API_BASE}/camera/start`)
          cameraActive.value = true
          sessionStartTime.value = new Date()
        }
      } catch (error) {
        console.error('Error toggling camera:', error)
        alert('Error controlling camera: ' + error.message)
      } finally {
        loading.value = false
      }
    }
    
    // Export data
    const exportData = async () => {
      try {
        const response = await axios.post(`${API_BASE}/export/json`)
        alert(response.data.message)
      } catch (error) {
        console.error('Error exporting data:', error)
        alert('Error exporting data: ' + error.message)
      }
    }    // Open student history modal
    const openStudentHistory = (faceId) => {
      selectedFaceId.value = faceId
      showHistoryModal.value = true
      
      // Initialize chart if student has history data
      if (studentHistory[faceId] && studentHistory[faceId].length > 0) {
        // Give the DOM time to render before initializing the chart
        setTimeout(() => {
          console.log('Attempting to initialize chart for face ID:', faceId)
          console.log('History data points:', studentHistory[faceId].length)
          
          // Ensure Chart.js is loaded
          if (typeof Chart === 'undefined') {
            const script = document.createElement('script')
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js'
            script.onload = () => {
              console.log('Chart.js loaded in modal, initializing chart now')
              initHistoryChart(faceId)
            }
            script.onerror = (err) => {
              console.error('Failed to load Chart.js in modal:', err)
            }
            document.head.appendChild(script)
          } else {
            initHistoryChart(faceId)
          }
        }, 100) // Increased timeout for more reliable rendering
      } else {
        console.warn('No history data available for face ID:', faceId)
      }
    }// Initialize history chart
    const initHistoryChart = (faceId) => {
      const historyData = studentHistory[faceId]
      if (!historyData || historyData.length === 0) {
        console.warn('No history data available for chart')
        return
      }
      
      // Explicitly load Chart.js if not already loaded
      if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded yet, loading now and retrying in 1000ms')
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js'
        script.onload = () => {
          console.log('Chart.js loaded dynamically, initializing chart')
          setTimeout(() => initHistoryChart(faceId), 100)
        }
        document.head.appendChild(script)
        return
      }
      
      const canvas = document.getElementById('historyChart')
      if (!canvas) {
        console.warn('Canvas element not found, retrying in 200ms')
        setTimeout(() => initHistoryChart(faceId), 200)
        return
      }
      
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Could not get 2D context from canvas')
        return
      }
        // Clear any existing chart
      try {
        if (window.historyChart && typeof window.historyChart.destroy === 'function') {
          window.historyChart.destroy();
        }
      } catch (error) {
        console.error('Error destroying existing chart:', error);
      }
      // Always reset the history chart reference
      window.historyChart = null;
      
      // Prepare data with simple numeric labels
      const labels = historyData.map((_, i) => i + 1)
      const concentrationData = historyData.map(entry => parseFloat(entry.concentration) || 0)
      
      console.log('Creating chart with data points:', concentrationData.length, 'First point:', concentrationData[0])      // Create chart
      try {
        window.historyChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: 'Concentration %',
              data: concentrationData,
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderWidth: 2,
              tension: 0.3,
              fill: true
            }]
          },
          options: {
            animation: {
              duration: 1000
            },
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    return `Concentration: ${context.raw}%`;
                  }
                }
              }
            },
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                  callback: function(value) {
                    return value + '%'
                  }
                }
              },
              x: {
                title: {
                  display: true,
                  text: 'Detection Points'
                }
              }
            }
          }
        });
        console.log('Chart successfully created');
      } catch (error) {
        console.error('Error creating chart:', error);
      }
    }
      // Utility functions
    const getConcentrationClass = (concentration) => {
      if (concentration >= 70) return 'concentration-high'
      if (concentration >= 40) return 'concentration-medium'
      return 'concentration-low'
    }
    
    const getConcentrationBarClass = (concentration) => {
      if (concentration >= 70) return 'bg-success-500'
      if (concentration >= 40) return 'bg-warning-500'
      return 'bg-danger-500'
    }
      // Function to get face image from currentDetections or history
    const getFaceImage = (faceId) => {
      // First try to find in current detections
      const detection = currentDetections.value.find(d => d.face_id === faceId);
      if (detection && detection.face_image) {
        // Update history with latest image
        faceImagesHistory[faceId] = detection.face_image;
        return detection.face_image;
      }
      
      // If not found in current detections, use stored history
      return faceImagesHistory[faceId] || null;
    }
    
    const formatTime = (timeString) => {
      return new Date(timeString).toLocaleTimeString()
    }
    
    const formatSessionTime = () => {
      const now = new Date()
      const diff = Math.floor((now - sessionStartTime.value) / 1000)
      const minutes = Math.floor(diff / 60)
      const seconds = diff % 60
      return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
    }
      // Lifecycle hooks
    onMounted(() => {
      initWebSocket()
      fetchFaces()
      fetchStatistics()
      loadFaceImagesHistory() // Load face images history on mount
      
      // Add Chart.js script if not already added
      if (!document.getElementById('chartjs')) {
        const script = document.createElement('script')
        script.id = 'chartjs'
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
        script.async = true
        
        // Ensure script is loaded before trying to use Chart
        script.onload = () => {
          console.log('Chart.js loaded successfully')
        }
        script.onerror = () => {
          console.error('Failed to load Chart.js')
        }
        
        document.head.appendChild(script)
      }
      
      // Periodically update session time
      setInterval(() => {
        // This will trigger reactivity for session time
      }, 1000)
    })
    onUnmounted(() => {
      if (ws) {
        ws.close()
      }
    })
      return {
      faces,
      statistics,
      currentFrame,
      currentDetections,
      cameraActive,
      connectionStatus,
      handleImageError,
      loading,
      toggleCamera,
      exportData,
      getConcentrationClass,
      getConcentrationBarClass,
      formatTime,
      formatSessionTime,
      getFaceImage,
      handleImageError,
      faceImagesHistory,
      studentHistory,
      selectedFaceId,
      showHistoryModal,
      openStudentHistory
    }
  }
}
</script>

<style scoped>
.student-face-image {
  transition: all 0.3s ease;
}

/* Card hover effect */
.cursor-pointer:hover .student-face-image {
  transform: scale(1.05);
}

/* Concentration classes */
.concentration-high {
  color: #10b981;
}

.concentration-medium {
  color: #f59e0b;
}

.concentration-low {
  color: #ef4444;
}

/* Emotion badges */
.emotion-badge {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
  background-color: #e5e7eb;
}

.emotion-happy {
  background-color: #fef3c7;
  color: #92400e;
}

.emotion-sad {
  background-color: #e0e7ff;
  color: #3730a3;
}

.emotion-angry {
  background-color: #fee2e2;
  color: #b91c1c;
}

.emotion-neutral {
  background-color: #e5e7eb;
  color: #374151;
}

.emotion-surprised {
  background-color: #fce7f3;
  color: #9d174d;
}

/* Modal animation */
.fixed {
  animation: fadeIn 0.2s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Chart container */
.chart-container {
  position: relative;
  height: 100%;
  width: 100%;
}

#historyChart {
  max-width: 100%;
  height: 100% !important;
  width: 100% !important;
}

/* Make sure modal is properly sized for small screens */
@media (max-width: 640px) {
  .fixed > div:not(.fixed) {
    width: 90%;
    max-width: 90%;
    margin: 0 auto;
  }
}
</style>
