# Implementing a Custom Confirmation Modal

You are currently using the browser's native `confirm()` function. To upgrade this to a nice looking custom modal, follow these steps.

## 1. Add the Modal HTML
Add this code at the bottom of your HTML file, just before the `<script>` tags (similar to your existing `addModal` and `editModal`).

```html
<!-- Approve Confirmation Modal -->
<div id="approveModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
  <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
    <!-- Modal Header -->
    <div class="p-6 border-b flex items-center gap-3">
      <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
        <i class="fas fa-check text-green-600 text-xl"></i>
      </div>
      <h3 class="text-xl font-bold text-gray-900">Approve Property?</h3>
    </div>

    <!-- Modal Body -->
    <div class="p-6">
      <p class="text-gray-600">
        Are you sure you want to approve this property? It will become visible on the public site immediately.
      </p>
    </div>

    <!-- Modal Footer -->
    <div class="p-4 bg-gray-50 rounded-b-lg flex justify-end gap-3">
      <button onclick="closeApproveModal()" 
        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100 font-medium">
        Cancel
      </button>
      <button onclick="confirmApprove()" 
        class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold shadow-sm">
        Yes, Approve It
      </button>
    </div>
  </div>
</div>
```

## 2. Update Your JavaScript
You need to split your logic into:
1. Opening the modal (and saving the ID).
2. Actually performing the action when "Yes" is clicked.

Replace your existing [approveProperty](file:///c:/Users/francis/OneDrive/Desktop/DJANGO%20PROJECT/realestate/templates/admin/dirty_properties.html#469-492) function with this:

```javascript
  let propertyIdToApprove = null; // Variable to store the ID temporarily

  // 1. Triggered by the button in the table
  function openApproveModal(id) {
    propertyIdToApprove = id; // Save the ID
    document.getElementById('approveModal').classList.remove('hidden'); // Show modal
  }

  // 2. Triggered by "Cancel"
  function closeApproveModal() {
    propertyIdToApprove = null; // Clear ID
    document.getElementById('approveModal').classList.add('hidden'); // Hide modal
  }

  // 3. Triggered by "Yes, Approve It" inside the modal
  function confirmApprove() {
    if (!propertyIdToApprove) return;

    // Use the stored ID for the API call
    fetch(`/api/approve_property/${propertyIdToApprove}`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}'
      },
    })
    .then(response => {
      if (response.ok) {
        // Optional: Show a success message or toast here
        location.reload(); 
      } else {
        alert('Failed to approve property');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while approving property');
    })
    .finally(() => {
      closeApproveModal(); // Cleanup
    });
  }
```

## 3. Update the Button in the Table
Finally, update the button in your table loop to call `openApproveModal` instead of [approveProperty](file:///c:/Users/francis/OneDrive/Desktop/DJANGO%20PROJECT/realestate/templates/admin/dirty_properties.html#469-492).

```html
<!-- Old -->
<!-- <button onclick="approveProperty({{property.id}})" ... > -->

<!-- New -->
<button onclick="openApproveModal({{property.id}})" class="text-green-600 hover:text-green-700 p-2" title="Approve">
  <i class="fas fa-check"></i>
</button>
```
