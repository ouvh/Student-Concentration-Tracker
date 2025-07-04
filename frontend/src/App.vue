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
              <h1 class="text-2xl font-bold text-gray-900">AI Learning Assistant</h1>
              <p class="text-sm text-gray-600">Emotion tracking & sign language translation</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 rounded-full" :class="connectionStatus ? 'bg-green-500' : 'bg-red-500'"></div>
              <span class="text-sm text-gray-600">{{ connectionStatus ? 'Connected' : 'Disconnected' }}</span>
            </div>
            
            <button 
              @click="showResetConfirmModal = true"
              class="btn-warning"
              :disabled="loading"
              title="Reset all data and clear database"
            >
              <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Reset All Data
            </button>
            
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
        
        <!-- Tab Navigation -->
        <div class="border-t border-gray-200">
          <nav class="flex space-x-8" aria-label="Tabs">
            <button
              @click="activeTab = 'concentration'"
              :class="activeTab === 'concentration' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors"
            >
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              Concentration Tracking
            </button>
            <button
              @click="activeTab = 'signlanguage'"
              :class="activeTab === 'signlanguage' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors"
            >
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>
              </svg>
              Sign Language Translation
            </button>
          </nav>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Concentration Tracking Tab -->
      <div v-if="activeTab === 'concentration'">
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

        <!-- Right Panel - Emotion Distribution and Device Detection -->
        <div class="space-y-6">
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

          <!-- Device Detection Panel -->
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900">
                <svg class="w-5 h-5 inline mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                </svg>
                Device Detection
              </h3>
              <div class="flex items-center space-x-3">
                <!-- Device Tracking Toggle -->
                <button 
                  @click="toggleDeviceTracking"
                  :class="deviceTrackingEnabled ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-400 hover:bg-gray-500'"
                  class="px-3 py-1 text-xs text-white rounded-full transition-colors flex items-center space-x-1"
                  :title="deviceTrackingEnabled ? 'Click to disable device tracking' : 'Click to enable device tracking'"
                >
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="deviceTrackingEnabled" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                  </svg>
                  <span>{{ deviceTrackingEnabled ? 'ON' : 'OFF' }}</span>
                </button>
                
                <!-- Status Indicator -->
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 rounded-full animate-pulse" :class="deviceTrackingEnabled && deviceSummary.total_devices > 0 ? 'bg-red-500' : deviceTrackingEnabled ? 'bg-green-500' : 'bg-gray-400'"></div>
                  <span class="text-xs font-medium" :class="deviceTrackingEnabled && deviceSummary.total_devices > 0 ? 'text-red-600' : deviceTrackingEnabled ? 'text-green-600' : 'text-gray-500'">
                    {{ !deviceTrackingEnabled ? 'DISABLED' : deviceSummary.total_devices > 0 ? 'ACTIVE' : 'CLEAR' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Overall Status -->
            <div class="mb-4 p-3 rounded-lg" :class="getOverallStatusBg()">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="text-2xl">{{ getDistractionIcon() }}</span>
                  <div>
                    <p class="font-semibold" :class="getDistractionTextClass()">
                      {{ deviceDistractionText }} Distraction
                    </p>
                    <p class="text-sm text-gray-600">
                      {{ deviceSummary.total_devices }} device{{ deviceSummary.total_devices !== 1 ? 's' : '' }}
                    </p>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-xl font-bold" :class="getDistractionTextClass()">
                    {{ deviceSummary.total_devices }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Device Types Grid -->
            <div v-if="deviceTrackingEnabled && Object.keys(deviceSummary.devices).length > 0" class="grid grid-cols-2 gap-2 mb-4">
              <div 
                v-for="(count, deviceType) in deviceSummary.devices" 
                :key="deviceType"
                @click="openDeviceTypeHistory(deviceType)"
                class="cursor-pointer bg-gray-50 hover:bg-blue-50 rounded-lg p-3 border hover:border-blue-300 transition-all transform hover:scale-105 group"
                :title="`Click to view ${formatDeviceType(deviceType)} detection history`"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-6 h-6 rounded flex items-center justify-center group-hover:scale-110 transition-transform" 
                         :style="{ backgroundColor: getDeviceColor(deviceType) + '20' }">
                      <svg class="w-4 h-4" :style="{ color: getDeviceColor(deviceType) }" fill="currentColor" viewBox="0 0 20 20">
                        <path v-if="deviceType === 'smartphone'" d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 011 1v8a1 1 0 01-1 1H5a1 1 0 01-1-1V7z"></path>
                        <path v-else-if="deviceType === 'laptop'" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1h-1l1 2h-14l1-2H4a1 1 0 01-1-1V4z"></path>
                        <path v-else-if="deviceType === 'tablet'" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V4a2 2 0 00-2-2H6z"></path>
                        <path v-else-if="deviceType === 'book'" d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
                        <path v-else-if="deviceType === 'mouse'" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm2 1v6h10V5H5z"></path>
                        <path v-else-if="deviceType === 'keyboard'" d="M4 5a2 2 0 00-2 2v6a2 2 0 002 2h12a2 2 0 002-2V7a2 2 0 00-2-2H4zm0 2h12v6H4V7z"></path>
                        <path v-else d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4z"></path>
                      </svg>
                    </div>
                    <span class="text-sm font-medium capitalize group-hover:text-blue-600 transition-colors">{{ formatDeviceType(deviceType) }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <span class="text-lg font-bold group-hover:scale-110 transition-transform" :style="{ color: getDeviceColor(deviceType) }">
                      {{ count }}
                    </span>
                    <svg class="w-3 h-3 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Device Tracking Disabled State -->
            <div v-else-if="!deviceTrackingEnabled" class="text-center py-6">
              <div class="w-12 h-12 mx-auto mb-2 bg-gray-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                </svg>
              </div>
              <p class="text-sm font-medium text-gray-600">Device Tracking Disabled</p>
              <p class="text-xs text-gray-500">Click the toggle button to enable</p>
            </div>
            
            <!-- No Devices State -->
            <div v-else class="text-center py-6">
              <div class="w-12 h-12 mx-auto mb-2 bg-green-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <p class="text-sm font-medium text-green-700">All Clear!</p>
              <p class="text-xs text-gray-500">No devices detected</p>
            </div>

            <!-- Quick Stats -->
            <div class="grid grid-cols-2 gap-2 pt-3 border-t border-gray-200">
              <div class="text-center">
                <div class="text-sm font-bold text-gray-700">{{ deviceStats.total_detections }}</div>
                <div class="text-xs text-gray-500">Total</div>
              </div>
              <div class="text-center">
                <div class="text-sm font-bold text-gray-700">{{ deviceStats.avg_devices_per_detection.toFixed(1) }}</div>
                <div class="text-xs text-gray-500">Average</div>
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
      
      <!-- End of Concentration Tab -->
      </div>

      <!-- Sign Language Translation Tab -->
      <div v-if="activeTab === 'signlanguage'">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Sign Language Camera Feed -->
          <div class="card">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-semibold text-gray-900">Sign Language Camera</h2>
              <div class="flex items-center space-x-2">
                <div class="w-2 h-2 rounded-full animate-pulse" :class="signLanguageActive ? 'bg-green-500' : 'bg-red-500'"></div>
                <span class="text-sm text-gray-600">{{ signLanguageActive ? 'ACTIVE' : 'INACTIVE' }}</span>
              </div>
            </div>
            
            <div class="aspect-video bg-gray-900 rounded-lg overflow-hidden relative mb-4">
              <img 
                v-if="signLanguageFrame" 
                :src="`data:image/jpeg;base64,${signLanguageFrame}`" 
                alt="Sign Language Feed"
                class="w-full h-full object-cover"
              />
              <div v-else class="flex items-center justify-center h-full">
                <div class="text-center text-gray-400">
                  <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h4a1 1 0 011 1v2m0 0V1a1 1 0 011-1h4a1 1 0 011 1v3M7 4H5a2 2 0 00-2 2v3m4-5a2 2 0 012 2v3m0 0V9a2 2 0 012 2v3m0 0h2a2 2 0 012-2v-3a2 2 0 00-2-2h-2"></path>
                  </svg>
                  <p>{{ signLanguageActive ? 'Waiting for sign language feed...' : 'Sign language detection is off' }}</p>
                </div>
              </div>
              
              <!-- Current Detection Overlay -->
              <div v-if="currentSignDetection" class="absolute top-4 left-4 right-4">
                <div class="bg-black bg-opacity-75 text-white px-4 py-2 rounded-lg">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium">Detected:</span>
                    <span class="text-lg font-bold">{{ currentSignDetection.sign }}</span>
                  </div>
                  <div class="flex items-center justify-between mt-1">
                    <span class="text-xs">Confidence:</span>
                    <span class="text-xs">{{ (currentSignDetection.confidence * 100).toFixed(1) }}%</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Sign Language Controls -->
            <div class="flex items-center justify-between">
              <button 
                @click="toggleSignLanguage" 
                :class="signLanguageActive ? 'btn-danger' : 'btn-success'"
                :disabled="loading"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path v-if="signLanguageActive" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ signLanguageActive ? 'Stop Detection' : 'Start Detection' }}
              </button>
              
              <div class="flex items-center space-x-2">
                <button 
                  @click="clearTranslatedText"
                  class="btn-secondary"
                  :disabled="translatedText.length === 0"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                  Clear Text
                </button>
                
                <button 
                  @click="copyTranslatedText"
                  class="btn-secondary"
                  :disabled="translatedText.length === 0"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                  </svg>
                  Copy
                </button>
              </div>
            </div>
          </div>
          
          <!-- Translation Output -->
          <div class="space-y-6">
            <!-- Translated Text Display -->
            <div class="card">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Translated Text</h3>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 rounded-full" :class="translatedText.length > 0 ? 'bg-green-500' : 'bg-gray-400'"></div>
                  <span class="text-sm text-gray-600">{{ translatedText.length }} characters</span>
                </div>
              </div>
              
              <div class="min-h-[200px] max-h-[400px] overflow-y-auto">
                <div v-if="translatedText.length === 0" class="flex items-center justify-center h-48 text-gray-400">
                  <div class="text-center">
                    <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"></path>
                    </svg>
                    <p class="text-sm">Translated text will appear here</p>
                  </div>
                </div>
                <div v-else class="prose prose-lg max-w-none">
                  <div 
                    class="bg-gray-50 rounded-lg p-4 border border-gray-200"
                    style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 16px; line-height: 1.6;"
                  >
                    {{ translatedText }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Sign Language Statistics -->
            <div class="card">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Detection Statistics</h3>
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <div class="text-2xl font-bold text-blue-600">{{ signLanguageStats.totalSigns }}</div>
                  <div class="text-sm text-gray-600">Total Signs</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <div class="text-2xl font-bold text-green-600">{{ signLanguageStats.wordsPerMinute }}</div>
                  <div class="text-sm text-gray-600">Words/Min</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <div class="text-2xl font-bold text-purple-600">{{ signLanguageStats.avgConfidence }}%</div>
                  <div class="text-sm text-gray-600">Avg Confidence</div>
                </div>
                <div class="bg-gray-50 rounded-lg p-3 text-center">
                  <div class="text-2xl font-bold text-orange-600">{{ signLanguageStats.uniqueSigns }}</div>
                  <div class="text-sm text-gray-600">Unique Signs</div>
                </div>
              </div>
            </div>
            
            <!-- Recent Detections -->
            <div class="card">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Detections</h3>
              <div class="space-y-2 max-h-48 overflow-y-auto">
                <div v-if="recentSignDetections.length === 0" class="text-center py-8 text-gray-400">
                  <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
                  </svg>
                  <p class="text-sm">No recent detections</p>
                </div>
                <div v-else>
                  <div 
                    v-for="(detection, index) in recentSignDetections.slice(0, 10)" 
                    :key="index"
                    class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <span class="text-blue-600 font-bold text-sm">{{ detection.sign.charAt(0).toUpperCase() }}</span>
                      </div>
                      <div>
                        <div class="font-medium text-gray-900">{{ detection.sign }}</div>
                        <div class="text-sm text-gray-500">{{ (detection.confidence * 100).toFixed(1) }}% confidence</div>
                      </div>
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ formatTimeAgo(detection.timestamp) }}
                    </div>
                  </div>
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

      <!-- Device Class History Modal -->
      <div v-if="showDeviceClassModal" class="fixed inset-0 flex items-center justify-center z-50">
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="showDeviceClassModal = false"></div>
        <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-2xl w-full mx-4 relative z-10 max-h-[90vh] overflow-y-auto">
          <!-- Modal Header -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center" 
                   :style="{ backgroundColor: getDeviceColor(selectedDeviceClass) + '20' }">
                <svg class="w-6 h-6" :style="{ color: getDeviceColor(selectedDeviceClass) }" fill="currentColor" viewBox="0 0 20 20">
                  <path v-if="selectedDeviceClass === 'cell phone'" d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 011 1v8a1 1 0 01-1 1H5a1 1 0 01-1-1V7z"></path>
                  <path v-else-if="selectedDeviceClass === 'laptop'" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1h-1l1 2h-14l1-2H4a1 1 0 01-1-1V4zm2 1v6h10V5H5z"></path>
                  <path v-else-if="selectedDeviceClass === 'tablet'" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V4a2 2 0 00-2-2H6zm0 2h8v8H6V4zm4 10a1 1 0 100 2 1 1 0 000-2z"></path>
                  <path v-else-if="selectedDeviceClass === 'book'" d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
                  <path v-else d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4z"></path>
                </svg>
              </div>
              <div>
                <h3 class="text-xl font-semibold text-gray-900 capitalize">
                  {{ formatDeviceType(selectedDeviceClass) }} History
                </h3>
                <p class="text-sm text-gray-500">Detection timeline</p>
              </div>
            </div>
            <button @click="showDeviceClassModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- Device Class Stats -->
          <div class="grid grid-cols-3 gap-3 mb-4">
            <div class="bg-gray-50 rounded-lg p-3 text-center">
              <div class="text-xl font-bold" :style="{ color: getDeviceColor(selectedDeviceClass) }">
                {{ getDeviceClassStats(selectedDeviceClass).total }}
              </div>
              <div class="text-xs text-gray-600">Total</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-3 text-center">
              <div class="text-xl font-bold text-gray-700">
                {{ getDeviceClassStats(selectedDeviceClass).avgPerHour }}
              </div>
              <div class="text-xs text-gray-600">Avg per Hour</div>
            </div>
            <div class="bg-gray-50 rounded-lg p-3 text-center">
              <div class="text-xl font-bold text-gray-700">
                {{ getDeviceClassStats(selectedDeviceClass).lastSeen }}
              </div>
              <div class="text-xs text-gray-600">Last Seen</div>
            </div>
          </div>

          <!-- Timeline Chart -->
          <div class="mb-6">
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Detection Timeline</h4>
            <div class="bg-gray-50 rounded-xl p-4">
              <div class="h-48 relative">
                <canvas ref="deviceClassChart" class="w-full h-full"></canvas>
              </div>
            </div>
          </div>

          <!-- Recent Detections -->
          <div>
            <h4 class="text-lg font-semibold text-gray-800 mb-3">Recent Detections</h4>
            <div class="max-h-48 overflow-y-auto">
              <div v-if="getDeviceClassHistory(selectedDeviceClass).length === 0" class="text-center py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6"></path>
                </svg>
                <p>No recent detections</p>
              </div>
              <div v-else class="space-y-2">
                <div 
                  v-for="(detection, index) in getDeviceClassHistory(selectedDeviceClass).slice(0, 10)" 
                  :key="index"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: getDeviceColor(selectedDeviceClass) }"></div>
                    <span class="text-sm font-medium text-gray-700">Detected</span>
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ formatTimeAgo(detection.timestamp) }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-200">
            <button 
              @click="clearDeviceClassHistory(selectedDeviceClass)"
              class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
            >
              Clear History
            </button>
            <button 
              @click="showDeviceClassModal = false"
              class="px-6 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Device Type History Modal -->
    <div v-if="showDeviceTypeModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="fixed inset-0 bg-black bg-opacity-50" @click="closeDeviceTypeModal"></div>
      <div class="bg-white rounded-lg shadow-xl p-6 max-w-4xl w-full max-h-[80vh] overflow-y-auto relative z-10 m-4">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 rounded-lg flex items-center justify-center" 
                 :style="{ backgroundColor: getDeviceColor(selectedDeviceType) + '20' }">
              <svg class="w-6 h-6" :style="{ color: getDeviceColor(selectedDeviceType) }" fill="currentColor" viewBox="0 0 20 20">
                <path v-if="selectedDeviceType === 'smartphone'" d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 011 1v8a1 1 0 01-1 1H5a1 1 0 01-1-1V7z"></path>
                <path v-else-if="selectedDeviceType === 'laptop'" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1h-1l1 2h-14l1-2H4a1 1 0 01-1-1V4z"></path>
                <path v-else-if="selectedDeviceType === 'tablet'" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V4a2 2 0 00-2-2H6z"></path>
                <path v-else-if="selectedDeviceType === 'book'" d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z"></path>
                <path v-else d="M3 4a1 1 0 011-1h12a1 1 0 011 1v8a1 1 0 01-1 1H4a1 1 0 01-1-1V4z"></path>
              </svg>
            </div>
            <div>
              <h3 class="text-xl font-semibold text-gray-900 capitalize">
                {{ formatDeviceType(selectedDeviceType) }} Detection History
              </h3>
              <p class="text-sm text-gray-500">Timeline and statistics</p>
            </div>
          </div>
          <button @click="closeDeviceTypeModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Statistics Cards -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold" :style="{ color: getDeviceColor(selectedDeviceType) }">
              {{ deviceTypeStats.total_detections || 0 }}
            </div>
            <div class="text-sm text-gray-600">Total Detections</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-gray-700">
              {{ deviceTypeStats.avg_per_hour || 0 }}
            </div>
            <div class="text-sm text-gray-600">Avg per Hour</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-gray-700">
              {{ deviceTypeStats.peak_count || 0 }}
            </div>
            <div class="text-sm text-gray-600">Peak Count</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-4 text-center">
            <div class="text-2xl font-bold text-gray-700">
              {{ deviceTypeStats.most_active_hour || 'N/A' }}
            </div>
            <div class="text-sm text-gray-600">Most Active Hour</div>
          </div>
        </div>

        <!-- Timeline -->
        <div class="mb-6">
          <h4 class="text-lg font-semibold text-gray-800 mb-3">Detection Timeline</h4>
          <div class="bg-gray-50 rounded-xl p-4">
            <div v-if="deviceTypeHistory.length === 0" class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6-4h6m-6 4h6m-6 4h6"></path>
              </svg>
              <p>No detection history available</p>
            </div>
            <div v-else class="space-y-2">
              <div 
                v-for="(detection, index) in deviceTypeHistory.slice(0, 20)" 
                :key="index"
                class="flex items-center justify-between p-3 bg-white rounded-lg hover:bg-blue-50 transition-colors"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: getDeviceColor(selectedDeviceType) }"></div>
                  <div>
                    <div class="text-sm font-medium text-gray-700">
                      {{ detection.device_count || 1 }} {{ formatDeviceType(selectedDeviceType) }}{{ detection.device_count > 1 ? 's' : '' }} detected
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ new Date(detection.timestamp).toLocaleDateString() }}
                    </div>
                  </div>
                </div>
                <div class="text-sm text-gray-500">
                  {{ new Date(detection.timestamp).toLocaleTimeString() }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <button 
            @click="closeDeviceTypeModal"
            class="px-6 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Reset Confirmation Modal -->
    <div v-if="showResetConfirmModal" class="fixed inset-0 flex items-center justify-center z-50">
      <div class="fixed inset-0 bg-black bg-opacity-50" @click="showResetConfirmModal = false"></div>
      <div class="bg-white rounded-lg shadow-xl p-6 max-w-md w-full relative z-10 m-4">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-gray-900">Reset All Data</h3>
          </div>
          <button @click="showResetConfirmModal = false" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="mb-6">
          <p class="text-gray-600 mb-4">
            Are you sure you want to reset all data? This action will:
          </p>
          <ul class="text-sm text-gray-600 space-y-2 ml-4">
            <li class="flex items-start">
              <span class="text-red-500 mr-2">•</span>
              Clear all tracked student faces and their history
            </li>
            <li class="flex items-start">
              <span class="text-red-500 mr-2">•</span>
              Remove all device detection history
            </li>
            <li class="flex items-start">
              <span class="text-red-500 mr-2">•</span>
              Delete the face recognition database
            </li>
            <li class="flex items-start">
              <span class="text-red-500 mr-2">•</span>
              Reset all statistics and metrics
            </li>
          </ul>
          <div class="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p class="text-sm font-medium text-yellow-800">
              ⚠️ This action cannot be undone!
            </p>
          </div>
        </div>

        <div class="flex justify-end space-x-3">
          <button 
            @click="showResetConfirmModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="resetAllData"
            :disabled="resetting"
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50"
          >
            <span v-if="resetting">Resetting...</span>
            <span v-else>Reset All Data</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
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
    
    // Device detection data
    const deviceSummary = reactive({
      devices: {},
      total_devices: 0,
      distraction_level: 'low',
      timestamp: new Date().toISOString()
    })
    
    const deviceStats = reactive({
      total_detections: 0,
      device_counts: {},
      avg_devices_per_detection: 0,
      peak_device_count: 0,
      avg_distraction_level: 'low'
    })

    const deviceHistory = ref([])
    const showDeviceModal = ref(false)
    const selectedDevice = ref(null)
    const deviceChart = ref(null)
    let deviceChartInstance = null

    // Enhanced device detection state
    const showDeviceClassModal = ref(false)
    const selectedDeviceClass = ref(null)
    const deviceClassChart = ref(null)
    let deviceClassChartInstance = null
    const showDeviceHistory = ref(false)
    const deviceHistoryChart = ref(null)
    let chartInstance = null

    // Device tracking state
    const deviceTrackingEnabled = ref(true)
    const showDeviceTypeModal = ref(false)
    const selectedDeviceType = ref(null)
    const deviceTypeHistory = ref([])
    const deviceTypeStats = ref({})

    // Reset functionality
    const showResetConfirmModal = ref(false)
    const resetting = ref(false)

    // Tab management
    const activeTab = ref('concentration')

    // Sign Language Translation state
    const signLanguageActive = ref(false)
    const signLanguageFrame = ref(null)
    const currentSignDetection = ref(null)
    const translatedText = ref('')
    const recentSignDetections = ref([])
    const signLanguageStats = reactive({
      totalSigns: 0,
      wordsPerMinute: 0,
      avgConfidence: 0,
      uniqueSigns: 0
    })
    const signLanguageStartTime = ref(null)
    const signLanguageHistory = ref([])

    // Computed properties
    const deviceDistractionText = computed(() => {
      const texts = { low: 'Low', medium: 'Medium', high: 'High' }
      return texts[deviceSummary.distraction_level] || 'Unknown'
    })

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
    
    // Device methods
    const formatDeviceType = (deviceType) => {
      const typeMap = {
        'cell phone': 'Phone',
        'laptop': 'Laptop',
        'tablet': 'Tablet',
        'book': 'Book',
        'mouse': 'Mouse',
        'keyboard': 'Keyboard',
        'monitor': 'Monitor'
      }
      return typeMap[deviceType] || deviceType.charAt(0).toUpperCase() + deviceType.slice(1)
    }

    const getDeviceColor = (deviceType) => {
      const colors = {
        'cell phone': '#EF4444',
        'laptop': '#10B981',
        'tablet': '#F59E0B',
        'book': '#8B5CF6',
        'mouse': '#3B82F6',
        'keyboard': '#6366F1',
        'monitor': '#06B6D4'
      }
      return colors[deviceType] || '#6B7280'
    }

    const getOverallStatusBg = () => {
      if (deviceSummary.total_devices === 0) return 'bg-green-50 border border-green-200'
      if (deviceSummary.distraction_level === 'low') return 'bg-yellow-50 border border-yellow-200'
      if (deviceSummary.distraction_level === 'medium') return 'bg-orange-50 border border-orange-200'
      return 'bg-red-50 border border-red-200'
    }

    const getDistractionIcon = () => {
      if (deviceSummary.total_devices === 0) return '✅'
      if (deviceSummary.distraction_level === 'low') return '⚠️'
      if (deviceSummary.distraction_level === 'medium') return '⚠️'
      return '🚨'
    }

    const getDistractionTextClass = () => {
      if (deviceSummary.total_devices === 0) return 'text-green-700'
      if (deviceSummary.distraction_level === 'low') return 'text-yellow-700'
      if (deviceSummary.distraction_level === 'medium') return 'text-orange-700'
      return 'text-red-700'
    }

    // WebSocket connection
    let ws = null
    const API_BASE = 'http://localhost:8000'

    // Enhanced WebSocket message handling for devices
    const enhancedWSHandler = (event) => {
      try {
        const message = JSON.parse(event.data)
        if (message.type === 'detection_update') {
          const data = message.data
          
          // Handle existing emotion detection
          if (data.frame) {
            currentFrame.value = data.frame
          }
          if (data.detections) {
            currentDetections.value = data.detections
            
            // Store face images and history
            data.detections.forEach(detection => {
              if (detection.face_id && detection.face_image) {
                faceImagesHistory[detection.face_id] = detection.face_image
                
                if (detection.emotion && detection.concentration !== undefined) {
                  if (!studentHistory[detection.face_id]) {
                    studentHistory[detection.face_id] = []
                  }
                  studentHistory[detection.face_id].push({
                    timestamp: new Date(),
                    emotion: detection.emotion,
                    concentration: detection.concentration
                  })
                  
                  // Limit history size
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
          
          // Handle device detection data
          if (data.devices) {
            Object.assign(deviceSummary, {
              devices: data.devices.device_counts || {},
              total_devices: data.devices.total_devices || 0,
              distraction_level: data.devices.distraction_level || 'low',
              timestamp: data.devices.timestamp || new Date().toISOString()
            })
          }
          
          if (data.statistics) {
            Object.assign(statistics, data.statistics)
          }
          
          fetchFaces()
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
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
      
      ws.onmessage = enhancedWSHandler
      
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
      // Device detection methods
    const fetchDeviceData = async () => {
      try {
        // Fetch current device summary
        const summaryResponse = await axios.get(`${API_BASE}/api/devices/current`)
        if (summaryResponse.data) {
          Object.assign(deviceSummary, summaryResponse.data)
        }

        // Fetch device statistics
        const statsResponse = await axios.get(`${API_BASE}/api/devices/statistics`)
        if (statsResponse.data) {
          Object.assign(deviceStats, statsResponse.data)
        }

        // Fetch device history if showing
        if (showDeviceModal.value) {
          const historyResponse = await axios.get(`${API_BASE}/api/devices/history?minutes=60`)
          if (historyResponse.data) {
            deviceHistory.value = historyResponse.data
            await nextTick()
            updateDeviceChart()
          }
        }
      } catch (error) {
        console.error('Error fetching device data:', error)
      }
    }

    const clearDeviceHistory = async () => {
      try {
        await axios.post(`${API_BASE}/api/devices/clear-history`)
        deviceHistory.value = []
        Object.assign(deviceStats, {
          total_detections: 0,
          device_counts: {},
          avg_devices_per_detection: 0,
          peak_device_count: 0,
          avg_distraction_level: 'low'
        })
        updateDeviceChart()
      } catch (error) {
        console.error('Error clearing device history:', error)
      }
    }

    // Device modal functions
    const openDeviceClassHistory = (deviceType) => {
      selectedDeviceClass.value = deviceType
      showDeviceClassModal.value = true
      
      // Initialize chart after modal opens
      nextTick(() => {
        initDeviceClassChart()
      })
    }

    const initDeviceClassChart = () => {
      if (typeof Chart === 'undefined') {
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
        script.onload = () => {
          setTimeout(initDeviceClassChart, 100)
        }
        document.head.appendChild(script)
        return
      }

      const canvas = deviceClassChart.value
      if (!canvas) return

      if (deviceClassChartInstance) {
        deviceClassChartInstance.destroy()
      }

      const ctx = canvas.getContext('2d')
      const history = getDeviceClassHistory(selectedDeviceClass.value)
      
      const labels = history.map((_, index) => index + 1)
      const data = history.map(entry => entry.devices[selectedDeviceClass.value] || 0)

      deviceClassChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Detections',
            data: data,
            borderColor: getDeviceColor(selectedDeviceClass.value),
            backgroundColor: getDeviceColor(selectedDeviceClass.value) + '20',
            borderWidth: 2,
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      })
    }

    const getDeviceClassHistory = (deviceType) => {
      return deviceHistory.value.filter(entry => 
        entry.devices && entry.devices[deviceType] > 0
      ).slice(-20)
    }

    const getDeviceClassStats = (deviceType) => {
      const history = getDeviceClassHistory(deviceType)
      const total = history.reduce((sum, entry) => sum + (entry.devices[deviceType] || 0), 0)
      const avgPerHour = history.length > 0 ? (total / (history.length / 12)).toFixed(1) : '0'
      const lastSeen = history.length > 0 ? formatTimeAgo(history[history.length - 1].timestamp) : 'Never'
      
      return { total, avgPerHour, lastSeen }
    }

    const clearDeviceClassHistory = async (deviceType) => {
      try {
        await axios.post(`${API_BASE}/api/devices/clear-history`)
        deviceHistory.value = []
        showDeviceClassModal.value = false
      } catch (error) {
        console.error('Error clearing device class history:', error)
      }
    }

    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const time = new Date(timestamp)
      const diffMinutes = Math.floor((now - time) / (1000 * 60))
      
      if (diffMinutes < 1) return 'Just now'
      if (diffMinutes < 60) return `${diffMinutes}m ago`
      if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`
      return `${Math.floor(diffMinutes / 1440)}d ago`
    }

    // Device tracking control methods
    const toggleDeviceTracking = async () => {
      try {
        const response = await axios.post(`${API_BASE}/api/devices/toggle-tracking?enabled=${!deviceTrackingEnabled.value}`)
        if (response.data) {
          deviceTrackingEnabled.value = response.data.tracking_enabled
          console.log(`Device tracking ${deviceTrackingEnabled.value ? 'enabled' : 'disabled'}`)
        }
      } catch (error) {
        console.error('Error toggling device tracking:', error)
      }
    }

    const fetchDeviceTrackingStatus = async () => {
      try {
        const response = await axios.get(`${API_BASE}/api/devices/tracking-status`)
        if (response.data) {
          deviceTrackingEnabled.value = response.data.tracking_enabled
        }
      } catch (error) {
        console.error('Error fetching device tracking status:', error)
      }
    }

    const openDeviceTypeHistory = async (deviceType) => {
      try {
        selectedDeviceType.value = deviceType
        showDeviceTypeModal.value = true
        
        // Fetch device type history
        const response = await axios.get(`${API_BASE}/api/devices/type-history/${deviceType}`)
        if (response.data) {
          deviceTypeHistory.value = response.data.history
          deviceTypeStats.value = response.data.statistics
        }
      } catch (error) {
        console.error('Error fetching device type history:', error)
      }
    }

    const closeDeviceTypeModal = () => {
      showDeviceTypeModal.value = false
      selectedDeviceType.value = null
      deviceTypeHistory.value = []
      deviceTypeStats.value = {}
    }

    // Reset functionality
    const resetAllData = async () => {
      try {
        resetting.value = true
        
        const response = await axios.post(`${API_BASE}/api/system/reset-all-data`)
        
        if (response.data) {
          // Clear local data
          faces.value = []
          Object.keys(faceImagesHistory).forEach(key => delete faceImagesHistory[key])
          Object.keys(studentHistory).forEach(key => delete studentHistory[key])
          
          // Reset device data
          Object.assign(deviceSummary, {
            devices: {},
            total_devices: 0,
            distraction_level: 'low',
            timestamp: new Date().toISOString()
          })
          
          Object.assign(deviceStats, {
            total_detections: 0,
            device_counts: {},
            avg_devices_per_detection: 0,
            peak_device_count: 0,
            avg_distraction_level: 'low'
          })
          
          // Reset statistics
          Object.assign(statistics, {
            total_faces: 0,
            total_detections: 0,
            avg_concentration: 0,
            emotion_distribution: {}
          })
          
          // Clear localStorage
          localStorage.removeItem('faceImagesHistory')
          
          showResetConfirmModal.value = false
          console.log('All data has been reset successfully')
          
          // Show success message (you can add a toast notification here)
          alert('All data has been reset successfully!')
        }
      } catch (error) {
        console.error('Error resetting data:', error)
        alert('Failed to reset data. Please try again.')
      } finally {
        resetting.value = false
      }
    }

    // Sign Language Translation methods
    let signLanguageWS = null
    
    const startSignLanguageWebSocket = () => {
      signLanguageWS = new WebSocket('ws://localhost:8000/ws/signlanguage')
      
      signLanguageWS.onopen = () => {
        console.log('Connected to sign language WebSocket')
        // Send start detection message
        signLanguageWS.send(JSON.stringify({
          action: 'start_detection'
        }))
      }
      
      signLanguageWS.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          
          if (message.type === 'frame_update') {
            signLanguageFrame.value = message.frame
          } else if (message.type === 'sign_detection') {
            const detection = message.data
            currentSignDetection.value = detection
            
            // Add to translated text if confidence is high enough
            if (detection.confidence > 0.5) {
              if (translatedText.value.length > 0) {
                translatedText.value += ' '
              }
              translatedText.value += detection.sign
              
              // Add to history
              recentSignDetections.value.push({
                sign: detection.sign,
                confidence: detection.confidence,
                timestamp: new Date()
              })
              
              // Keep only last 50 detections
              if (recentSignDetections.value.length > 50) {
                recentSignDetections.value = recentSignDetections.value.slice(-50)
              }
              
              // Update statistics
              updateSignLanguageStats()
            }
          } else if (message.type === 'status') {
            console.log('Sign language status:', message.message)
          } else if (message.type === 'error') {
            console.error('Sign language error:', message.message)
            alert('Sign language error: ' + message.message)
          }
        } catch (error) {
          console.error('Error parsing sign language WebSocket message:', error)
        }
      }
      
      signLanguageWS.onclose = () => {
        console.log('Sign language WebSocket disconnected')
        signLanguageFrame.value = null
        currentSignDetection.value = null
      }
      
      signLanguageWS.onerror = (error) => {
        console.error('Sign language WebSocket error:', error)
      }
    }
    
    const stopSignLanguageWebSocket = () => {
      if (signLanguageWS) {
        signLanguageWS.send(JSON.stringify({
          action: 'stop_detection'
        }))
        signLanguageWS.close()
        signLanguageWS = null
      }
    }
    
    const updateSignLanguageStats = () => {
      const totalSigns = recentSignDetections.value.length
      const uniqueSignsSet = new Set(recentSignDetections.value.map(d => d.sign))
      const totalConfidence = recentSignDetections.value.reduce((sum, d) => sum + d.confidence, 0)
      
      signLanguageStats.totalSigns = totalSigns
      signLanguageStats.uniqueSigns = uniqueSignsSet.size
      signLanguageStats.avgConfidence = totalSigns > 0 ? Math.round((totalConfidence / totalSigns) * 100) : 0
      
      // Calculate words per minute
      if (signLanguageStartTime.value) {
        const timeDiff = (new Date() - signLanguageStartTime.value) / 1000 / 60 // minutes
        signLanguageStats.wordsPerMinute = timeDiff > 0 ? Math.round(totalSigns / timeDiff) : 0
      }
    }
    
    const toggleSignLanguage = () => {
      signLanguageActive.value = !signLanguageActive.value
      
      if (signLanguageActive.value) {
        signLanguageStartTime.value = new Date()
        startSignLanguageWebSocket()
        console.log('Sign language detection started')
      } else {
        signLanguageFrame.value = null
        currentSignDetection.value = null
        stopSignLanguageWebSocket()
        console.log('Sign language detection stopped')
      }
    }

    const clearTranslatedText = () => {
      translatedText.value = ''
      recentSignDetections.value = []
      signLanguageHistory.value = []
      
      // Reset statistics
      Object.assign(signLanguageStats, {
        totalSigns: 0,
        wordsPerMinute: 0,
        avgConfidence: 0,
        uniqueSigns: 0
      })
      
      signLanguageStartTime.value = new Date()
    }

    const copyTranslatedText = async () => {
      try {
        await navigator.clipboard.writeText(translatedText.value)
        alert('Text copied to clipboard!')
      } catch (error) {
        console.error('Failed to copy text:', error)
        const textArea = document.createElement('textarea')
        textArea.value = translatedText.value
        document.body.appendChild(textArea)
        textArea.select()
        document.execCommand('copy')
        document.body.removeChild(textArea)
        alert('Text copied to clipboard!')
      }
    }

    const getDeviceHistory = (deviceType) => {
      return deviceHistory.value.filter(entry => 
        entry.devices && entry.devices[deviceType] > 0
      )
    }

    const getDeviceStats = (deviceType) => {
      const history = getDeviceHistory(deviceType)
      return {
        total: history.length,
        recent: history.slice(-5)
      }
    }

    const openDeviceModal = (deviceType) => {
      selectedDevice.value = deviceType
      showDeviceModal.value = true
      
      nextTick(() => {
        updateDeviceChart()
      })
    }

    const closeDeviceModal = () => {
      showDeviceModal.value = false
      selectedDevice.value = null
      if (deviceChartInstance) {
        deviceChartInstance.destroy()
        deviceChartInstance = null
      }
    }

    const getOverallStatusClass = () => {
      if (deviceSummary.total_devices === 0) return 'text-green-600'
      if (deviceSummary.distraction_level === 'low') return 'text-yellow-600'
      if (deviceSummary.distraction_level === 'medium') return 'text-orange-600'
      return 'text-red-600'
    }

    const deviceDistractionClass = computed(() => {
      if (deviceSummary.total_devices === 0) return 'text-green-600'
      if (deviceSummary.distraction_level === 'low') return 'text-yellow-600'
      if (deviceSummary.distraction_level === 'medium') return 'text-orange-600'
      return 'text-red-600'
    })

    const deviceDistractionBg = computed(() => {
      if (deviceSummary.total_devices === 0) return 'bg-green-50'
      if (deviceSummary.distraction_level === 'low') return 'bg-yellow-50'
      if (deviceSummary.distraction_level === 'medium') return 'bg-orange-50'
      return 'bg-red-50'
    })

    const updateDeviceChart = async () => {
      await nextTick()
      
      if (!deviceChart.value || !selectedDevice.value) return

      if (deviceChartInstance) {
        deviceChartInstance.destroy()
        deviceChartInstance = null
      }

      if (typeof Chart === 'undefined') {
        const script = document.createElement('script')
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
        script.onload = () => {
          setTimeout(updateDeviceChart, 100)
        }
        document.head.appendChild(script)
        return
      }

      const ctx = deviceChart.value.getContext('2d')
      const history = getDeviceHistory(selectedDevice.value).slice(0, 20).reverse()
      
      const labels = history.map((_, index) => index + 1)
      const data = history.map(entry => entry.devices[selectedDevice.value] || 0)

      deviceChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Detections',
            data: data,
            borderColor: getDeviceColor(selectedDevice.value),
            backgroundColor: getDeviceColor(selectedDevice.value) + '20',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointRadius: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: { display: false },
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
                callback: function(value) {
                  return Number.isInteger(value) ? value : ''
                }
              }
            }
          }
        }
      })
    }

    // Initialize WebSocket
    onMounted(() => {
      initWebSocket()
      fetchFaces()
      fetchStatistics()
      loadFaceImagesHistory()
      fetchDeviceData()
      fetchDeviceTrackingStatus()
      
      // Load Chart.js
      if (!document.getElementById('chartjs')) {
        const script = document.createElement('script')
        script.id = 'chartjs'
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
        script.async = true
        document.head.appendChild(script)
      }

      // Set up periodic device data refresh
      setInterval(() => {
        fetchDeviceData()
      }, 5000) // Refresh every 5 seconds

      // Periodically update session time
      setInterval(() => {
        // This will trigger reactivity for session time
      }, 1000)
    })

    onUnmounted(() => {
      if (ws) {
        ws.close()
      }
      if (signLanguageWS) {
        signLanguageWS.close()
      }
      if (chartInstance) {
        chartInstance.destroy()
      }
      if (deviceChartInstance) {
        deviceChartInstance.destroy()
      }
    })

    // Add missing utility functions
    const getConcentrationClass = (concentration) => {
      if (concentration >= 70) return 'concentration-high'
      if (concentration >= 40) return 'concentration-medium'
      return 'concentration-low'
    }
    
    const getConcentrationBarClass = (concentration) => {
      if (concentration >= 70) return 'bg-green-500'
      if (concentration >= 40) return 'bg-yellow-500'
      return 'bg-red-500'
    }
      
    const getFaceImage = (faceId) => {
      const detection = currentDetections.value.find(d => d.face_id === faceId)
      if (detection && detection.face_image) {
        faceImagesHistory[faceId] = detection.face_image
        return detection.face_image
      }
      return faceImagesHistory[faceId] || null
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

    const watchDeviceHistory = () => {
      if (showDeviceHistory.value) {
        fetchDeviceData()
      }
    }

    return {
      faces,
      statistics,
      currentFrame,
      currentDetections,
      cameraActive,
      connectionStatus,
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
      openStudentHistory,
      // Device detection exports
      deviceSummary,
      deviceStats,
      deviceHistory,
      showDeviceModal,
      selectedDevice,
      deviceChart,
      formatDeviceType,
      getDeviceColor,
      getOverallStatusBg,
      getDistractionIcon,
      getDistractionTextClass,
      openDeviceModal,
      closeDeviceModal,
      getDeviceHistory,
      getDeviceStats,
      clearDeviceHistory,
      formatTimeAgo,
      deviceDistractionText,
      // Device tracking control exports
      deviceTrackingEnabled,
      toggleDeviceTracking,
      fetchDeviceTrackingStatus,
      openDeviceTypeHistory,
      closeDeviceTypeModal,
      showDeviceTypeModal,
      selectedDeviceType,
      deviceTypeHistory,
      deviceTypeStats,
      // Reset functionality exports
      showResetConfirmModal,
      resetting,
      resetAllData,
      // Tab management
      activeTab,
      // Sign language exports
      signLanguageActive,
      signLanguageFrame,
      currentSignDetection,
      translatedText,
      recentSignDetections,
      signLanguageStats,
      toggleSignLanguage,
      clearTranslatedText,
      copyTranslatedText
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

/* Enhanced device cards */
.group:hover {
  transform: translateY(-2px);
}

/* Smooth animations */
* {
  transition: all 0.2s ease;
}

/* Custom scrollbar for modal */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Button styles */
.btn-success {
  background-color: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-success:hover {
  background-color: #059669;
}

.btn-success:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-danger {
  background-color: #ef4444;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-danger:hover {
  background-color: #dc2626;
}

.btn-warning {
  background-color: #f59e0b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
}

.btn-warning:hover {
  background-color: #d97706;
}

.btn-warning:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
}

.btn-secondary:hover {
  background-color: #4b5563;
}

.card {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

/* Primary colors */
.bg-primary-100 {
  background-color: #dbeafe;
}

.bg-primary-600 {
  background-color: #2563eb;
}

.text-primary-600 {
  color: #2563eb;
}

.bg-success-100 {
  background-color: #dcfce7;
}

.text-success-600 {
  color: #16a34a;
}

.bg-warning-100 {
  background-color: #fef3c7;
}

.text-warning-600 {
  color: #d97706;
}
</style>
